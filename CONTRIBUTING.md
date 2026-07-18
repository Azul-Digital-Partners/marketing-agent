# Contributing to marketing-agent

Thank you for your interest in contributing! This project welcomes bug reports, feature requests, and pull requests.

## Reporting Issues

### Bug Reports

File a bug if something doesn't work as expected:

1. Use [GitHub Issues](../../issues)
2. Click "New issue" and select "Bug report"
3. Include:
   - What you tried
   - What you expected
   - What happened instead
   - Your OS and Python version
   - Relevant error messages or logs

**Example:**
```
/write "AI marketing trends" produces empty output instead of article

Expected: 2000+ word article saved to drafts/
Actual: Empty file created
Error: [paste error message]
OS: macOS 14.3
Python: 3.11.4
```

### Feature Requests

Have an idea for a new skill, command, or capability?

1. Use [GitHub Issues](../../issues)
2. Click "New issue" and select "Feature request"
3. Describe:
   - What you want to do
   - Why it would be useful
   - Rough idea for how it might work

**Example:**
```
Add /podcast-summary command — convert blog articles to podcast episode scripts

Use case: Repurposing written content into audio content.
Suggested flow: Parse article → generate podcast intro/outro → create segment scripts
```

## Submitting Pull Requests

### Before You Start

1. **Read the codebase** — Check `tools/`, `.claude/skills/`, and `.claude/commands/` to understand patterns
2. **Keep it focused** — One feature or fix per PR
3. **Test locally** — Make sure your changes work in Claude Code

### Adding a New Skill

Skills live in `.claude/skills/`. Copy an existing skill and modify:

```
.claude/skills/my-skill/
├── SKILL.md          # Skill definition, prompt, examples
└── tools/            # Python modules this skill uses (if any)
```

**Example SKILL.md structure:**
```markdown
# My Skill

One-line description.

## What it does

2-3 sentences.

## Usage

/my-skill [parameter]

## Process

Step 1: ...
Step 2: ...
Step 3: ...

## Output

What gets returned or saved.

## Examples

Example 1
Example 2
```

### Adding a New Command

Commands live in `.claude/commands/`. Follow the same structure as existing `.md` files. Commands automatically route to skills or tools based on naming.

### Adding a Python Module

If your contribution needs Python code:

1. Add to `tools/` or `data_sources/` depending on purpose
2. Include docstrings and type hints
3. Add dependencies to `data_sources/requirements.txt` if external packages needed
4. Test that existing commands still work

### Submission Checklist

- [ ] Code follows the patterns in existing skills/commands
- [ ] No API keys or credentials in the PR
- [ ] Updated README.md if adding a major feature
- [ ] Tested in Claude Code (not just locally)
- [ ] Clear commit message describing what and why

### Creating a PR

```bash
git checkout -b feature/my-feature
# ... make changes ...
git commit -m "Add my-feature: brief description"
git push origin feature/my-feature
```

Then go to GitHub and create a pull request. Link any related issues.

## Code Style

- **Markdown**: Keep it readable. Use clear headings, code blocks, and examples.
- **Python**: Standard PEP 8. Use type hints where possible.
- **Prompts**: Be specific. Reference context files, output format, and edge cases.

## Questions?

Open an issue with your question. We're here to help.

## License

By contributing, you agree your work will be licensed under the MIT License (see [LICENSE](LICENSE)).
