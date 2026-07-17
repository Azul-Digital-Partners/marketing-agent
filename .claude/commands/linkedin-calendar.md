# /linkedin-calendar

Generates a LinkedIn content calendar using the `linkedin-intelligence` skill.

## Behavior

1. Check whether `config/li_voice_profile.md` exists.

   **If it exists:** Read it before starting. Tell the user:
   > "I found your voice profile from a previous session. I'll use it as the starting point — you can update it during the interview or skip to the calendar."
   Then offer: run the full interview again, or skip straight to calendar generation using the existing profile.

   **If it does not exist:** Run the full `linkedin-intelligence` skill interview (all phases). At the end, save the completed voice profile to `config/li_voice_profile.md`.

2. After the interview (or if skipping), generate:
   - A 4–6 week content calendar saved to `output/linkedin-calendar-[YYYY-MM-DD].md`
   - Full post drafts for weeks 1–2 included in the same file

3. Confirm the file path to the user. Remind them: posting is manual — the calendar is a guide, not a schedule.

## Output file format

Save to `output/linkedin-calendar-YYYY-MM-DD.md`. Include:
- Voice profile summary (short — 5 lines)
- Pillar map
- Full calendar table (4–6 weeks)
- Week 1 and Week 2 post drafts, copy-paste ready
