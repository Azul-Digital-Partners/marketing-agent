# Manager / Executor Handoff

This folder splits marketing work into two roles.

- **Manager agent (Nadia).** Decides what gets done, in what order, and whether it is good enough. Lives in Notion. Never writes drafts.
- **Executor (Claude Code project, this repo).** Does the work. Research, drafts, rewrites, data pulls. Never decides priorities or publishes.

Steven approves anything that goes outside the company. Neither agent publishes on its own status.

## Files

| File | Who reads it | Purpose |
| --- | --- | --- |
| `manager-brief.md` | Nadia | Her job description as manager. Paste into her instructions. |
| `executor-rules.md` | Claude Code | Operating rules. Import from `CLAUDE.md`. |
| `task-brief-template.md` | Both | The format Nadia uses to hand off a task. |
| `report-template.md` | Both | The format Claude Code uses to hand work back. |
| `first-backlog.md` | Nadia | The first tasks to dispatch, in order. |

## Setup steps

1. **Configure the workspace first.** `context/brand-voice.md` still holds template text. Open this repo in Claude Code and run `/setup`. Every `/write` and `/research` output is generic until you do.
2. **Copy your real context in.** If your live `Marketing/context/` files exist on your Mac (positioning, voice profile, UTM convention), copy them into `context/` here instead of re-interviewing. Those files beat a fresh `/setup`.
3. **Executor rules are wired.** `CLAUDE.md` already imports them with:
   `@handoff/executor-rules.md`
4. **Give Nadia her brief.** Paste `manager-brief.md` into her agent instructions. Add her row to Agent Roster in Notion with role "Marketing Manager".
5. **Create the task channel.** In Notion, add a `Marketing Tasks` view to Agent Tasks filtered to `Agent = Claude Code (Marketing)`. Nadia writes briefs there. Claude Code writes reports there.
6. **Dispatch task 1** from `first-backlog.md`. Check the report against `report-template.md`. If the report is missing a section, fix the template, not the agent.

## The one rule

Notion holds decisions. The repo holds files. A task is not done because a file exists. It is done when its Notion row says `Accepted`.
