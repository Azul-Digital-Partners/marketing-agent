# Reddit OAuth — Setup Runbook

Required for the weekly Reddit Intelligence Digest, and for surfacing live threads
worth engaging with.

## Why this needs a human step

- Reddit returns `403` to unauthenticated JSON requests (verified 2026-06-01).
- `search.rss` ignores the `q` parameter and returns unrelated results, so the RSS
  workaround cannot do keyword search. It is not fixable — it is the wrong endpoint.
- The pullpush.io archive mirror is ~12 months stale, so current-week signal
  requires the live API.
- Any OAuth app must be owned by a Reddit account, and signup is CAPTCHA + email
  gated. No agent can clear that gate, and automating it would violate Reddit's
  User Agreement.

So one human, one time, ~5 minutes.

## Read the identity model before you start

There are **two** Reddit identities in this system and they must never be the same
account.

| | Read identity (API app owner) | Engage identity (human) |
|---|---|---|
| Purpose | Owns the OAuth app, powers the digest | Comments on threads |
| Posts or comments? | **Never** | Yes, manually |
| Credentials in `.env`? | Yes | **Never** |
| Needs karma/history? | No | Yes — this is the whole point |

Why they are separate:

- If the account holding your `client_id` gets actioned for promotional
  commenting, the intel pipeline dies with it. Single point of failure.
- A fresh account with no history posting outbound links matches Reddit's spam
  fingerprint almost exactly. Such accounts get shadowbanned quietly — you keep
  commenting and nobody sees any of it, including you.
- Mods escalate to **domain-level bans**, which are far harder to reverse than an
  account ban and affect every account, including real ones.

The digest's job is to hand a human a ranked queue. It never posts.
The engagement playbook itself lives in `context/reddit-strategy.md` — read it
before commenting anywhere.

---

## 1. Create the read account

Do **not** use a personal or brand account.

1. Open an incognito/private window.
2. Go to <https://www.reddit.com/register/>.
3. Email: an inbox you control that isn't tied to a marketing identity (a
   `+reddit-bot` alias on a Google Workspace inbox is fine).
4. Username: something like `<product>_intel_bot` — does **not** need to match a
   brand, and shouldn't.
5. Complete CAPTCHA, verify email, skip onboarding and subreddit picks.
6. **Never post or comment from this account.**

## 2. Create the app

1. Logged in as the read account, go to <https://www.reddit.com/prefs/apps>.
2. Bottom of page → **"are you a developer? create an app..."**
3. Fill in:
   - **name**: `<product>-market-intel`
   - **app type**: **script** — `installed` uses a different OAuth flow and cannot
     hold a secret
   - **description**: `Weekly market-intel digest (read-only)`
   - **about url**: your site
   - **redirect uri**: `http://localhost:8080` (required field; unused here)
4. Click **create app**, then capture:
   - **client_id** — the 22-character string under the app name, just below
     "personal use script"
   - **client_secret** — the `secret` field

## 3. Pick an auth flow

Two grants work with a `script` app. **Try app-only first** — it needs half as many
secrets and imposes no constraints on the account.

### Option A — app-only (`client_credentials`) — try this first

Needs only the client ID and secret. No account password stored anywhere, and no
restriction on enabling 2FA for the read account.

```bash
curl -s -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
  -A "$REDDIT_USER_AGENT" \
  -d "grant_type=client_credentials" \
  https://www.reddit.com/api/v1/access_token
```

A JSON body containing `access_token` means this works — use it and skip Option B.
An `error` field means fall back to Option B.

App-only tokens have historically carried tighter rate limits than user tokens.
For a weekly digest across a handful of subreddits this has not been a practical
constraint, but if you start seeing `429`s, that is the reason.

### Option B — password grant (ROPC) — fallback only

Needs the read account's username and password as well.

**If you use this flow, do not enable 2FA on the read account** — Reddit's script
flow does not support TOTP. This constraint is the main reason to prefer Option A.

```bash
curl -s -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
  -A "$REDDIT_USER_AGENT" \
  -d "grant_type=password&username=$REDDIT_USERNAME&password=$REDDIT_PASSWORD" \
  https://www.reddit.com/api/v1/access_token
```

## 4. Add credentials to `data_sources/config/.env`

Option A (app-only) needs only the first three:

```env
# Reddit API — read-only market intel. Owner: <bot-username>, app type: script
# Created: <yyyy-mm-dd>
REDDIT_CLIENT_ID=<22-char client_id from prefs/apps>
REDDIT_CLIENT_SECRET=<secret from prefs/apps>
REDDIT_USER_AGENT="<product>-market-intel/1.0 by /u/<bot-username>"

# Option B (password grant) only — omit these entirely if Option A worked
REDDIT_USERNAME=<bot-username>
REDDIT_PASSWORD=<bot-password>
```

**Quote the user agent.** It contains spaces, so an unquoted value makes
`set -a; . .env` silently export an *empty* string — and a missing UA is itself a
common cause of `403`. This is a real trap: nothing errors, the request just fails.

`REDDIT_USER_AGENT` must identify you. Reddit's canonical form is
`<platform>:<app id>:<version> (by /u/<username>)`; the simplified form above is
accepted. A generic or absent UA is a common cause of `429` and `403`.

## 5. Verify

From the repo root:

```bash
set -a; . data_sources/config/.env; set +a

TOKEN=$(curl -s -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
  -A "$REDDIT_USER_AGENT" \
  -d "grant_type=client_credentials" \
  https://www.reddit.com/api/v1/access_token \
  | python3 -c 'import json,sys;print(json.load(sys.stdin)["access_token"])')

curl -s -H "Authorization: Bearer $TOKEN" -A "$REDDIT_USER_AGENT" \
  "https://oauth.reddit.com/r/accessibility/search?q=ADA+lawsuit&t=week&restrict_sr=on&sort=new&limit=5" \
  | python3 -m json.tool | head -60
```

(Swap `grant_type` to the password form if you're on Option B.)

Three things prove the fix — check all of them, since the RSS failure mode was
returning plausible-looking junk:

1. A `Listing` with a non-empty `data.children`.
2. Every `created_utc` is within the last 7 days — confirms `t=week` is honoured.
3. Titles and bodies actually contain the query terms — **this is the check RSS
   failed.** `search.rss` returned a well-formed feed of irrelevant posts, which is
   why the health guards were needed.

Each post also carries `score`, `num_comments`, and `created_utc`. Those three
fields are the reason this path exists and DataForSEO SERP queries don't
substitute — index lag is days-to-weeks and engagement counts aren't available.

## 6. Feeding the engagement queue

Once search works, the digest should rank threads for a human to act on, not act
itself. Useful fields per row:

| Field | Why it matters |
|---|---|
| Thread URL + title | The target |
| Age in hours | Threads go quiet within ~24h; a 3-day-old thread rarely repays a comment |
| `score` / `num_comments` | Whether anyone is actually there |
| Matched keyword | Why it surfaced, so a human can dismiss false positives fast |
| Suggested angle | A draft for a human to rewrite — never an autopost |
| Subreddit self-promo rule | Most subs have one; many expect a ~9:1 non-promo ratio |

That last column is the one people skip and then get domain-banned over. Encode
each subreddit's rules in config once rather than rediscovering them.

Comment templates, what-not-to-do, and the "comment > post" rationale are all in
`context/reddit-strategy.md`.

## Security

- `.env` is gitignored (repo root `.gitignore`, `data_sources/config/.env`).
- Never echo these values into commits, comments, Slack, or standups.
- If the read account is suspended, rotate it — create a new one and re-register
  the app. Do not appeal, and do not log in from anywhere used for human posting.
