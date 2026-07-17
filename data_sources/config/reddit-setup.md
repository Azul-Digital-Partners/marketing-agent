# Reddit OAuth (script app) — Setup Runbook

Required for the weekly Reddit Intelligence Digest routine.

## Why this needs a human step

- Reddit blocks Anthropic's WebSearch UA and returns `403` to unauthenticated JSON requests (verified 2026-06-01 with custom UA from the host).
- The pullpush.io archive mirror is ~12 months stale, so current-week signal requires the live API.
- A `script` app needs a Reddit account that owns it. Signup is CAPTCHA + email + (often) phone-gated. No agent in the org can defeat that gate, and automating it would violate Reddit's User Agreement and risk the account being banned, breaking the routine.

So one human, one time, ~3 minutes.

## What to do (3-minute runbook)

### 1. Create a throwaway Reddit account — do **not** use [Your Name]'s personal account

1. Open an incognito/private window.
2. Go to <https://www.reddit.com/register/>.
3. Email: use an inbox you control that isn't tied to a marketing identity (a `+reddit-bot` alias on a Google Workspace inbox is fine).
4. Username suggestion: `[your product]_intel_bot` (or whatever's available — does **not** need to match any brand).
5. Complete CAPTCHA, verify email.
6. Skip any onboarding / subreddit picks. **Do not post or comment from this account** — it must remain a pure read-only identity.

### 2. Create the `script` app

1. Logged in as the bot account, go to <https://www.reddit.com/prefs/apps>.
2. Scroll to the bottom → **"are you a developer? create an app..."**.
3. Fill in:
   - **name**: `[your product]-market-intel`
   - **app type**: **script** (this is critical — `web` and `installed` use a different OAuth flow)
   - **description**: `Weekly market-intel digest for [your product] (read-only)`
   - **about url**: `https://[your product]app.com`
   - **redirect uri**: `http://localhost:8080` (required field; not used by the script flow)
4. Click **create app**.
5. Capture:
   - **client_id**: the 22-character string shown directly under the app name (just below "personal use script")
   - **client_secret**: the `secret` field

### 3. Paste this block into `Marketing/data_sources/config/.env`

```env
# Reddit API — script app credentials for weekly market intel digest
# App owner: <bot-username>, app type: script, scope: read
# Created: <yyyy-mm-dd>
REDDIT_CLIENT_ID=<22-char client_id from prefs/apps>
REDDIT_CLIENT_SECRET=<secret from prefs/apps>
REDDIT_USERNAME=<bot-username>
REDDIT_PASSWORD=<bot-password>
REDDIT_USER_AGENT=[your product]-market-intel/1.0 by /u/<bot-username>
```

Notes:

- Script-app OAuth uses ROPC (username + password), not refresh tokens. Do not enable 2FA on the bot account — Reddit's script flow does not support TOTP. If you must have 2FA, switch the app type to "web" and use a refresh token instead, but that's a code change in `data_sources/modules/` we'd need to plan separately.
- `REDDIT_USER_AGENT` must follow Reddit's format: `<platform>:<app id>:<version> (by /u/<username>)` is the canonical form; the value above is the simplified accepted form.

### 4. Verify

Once the `.env` block is in place, from the Marketing dir:

```bash
set -a; . data_sources/config/.env; set +a
TOKEN=$(curl -s -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
  -A "$REDDIT_USER_AGENT" \
  -d "grant_type=password&username=$REDDIT_USERNAME&password=$REDDIT_PASSWORD" \
  https://www.reddit.com/api/v1/access_token | python3 -c 'import json,sys;print(json.load(sys.stdin)["access_token"])')

curl -s -H "Authorization: Bearer $TOKEN" -A "$REDDIT_USER_AGENT" \
  "https://oauth.reddit.com/r/accessibility/search.json?q=ADA+lawsuit&t=week&restrict_sr=on&limit=5" \
  | python3 -m json.tool | head -40
```

You should see a `Listing` with `data.children` containing posts whose `created_utc` is within the last 7 days. This confirms the Reddit API integration is working correctly.

### 5. Notify

Once verified, the Reddit integration is ready for use in your marketing intelligence routines.

## Security

- `.env` is already gitignored under `Marketing/.gitignore`.
- Never echo any of the five values in issue comments, commit messages, Slack, or standups.
- If the bot account is ever banned or suspended, rotate by creating a new one — do not appeal, do not log in from anywhere that handles human-facing posting.
