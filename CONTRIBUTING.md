# Contributing to TestMu Skills

Thank you for your interest in contributing to the TestMu Skills repository! This guide will help you get started.

## Adding a New Skill

1. **Create a new directory** under the repository root:
   ```
   my-framework-skill/
   ├── SKILL.md           # Required — main skill file
   └── reference/
       ├── playbook.md    # Required — detailed implementation guide
       └── advanced-patterns.md  # Optional — advanced topics
   ```

2. **Write your SKILL.md** with proper YAML frontmatter:
   ```yaml
   ---
   name: my-framework-skill
   description: >
     Clear description of what the skill does and when to use it.
     Include trigger keywords in quotes.
   languages:
     - JavaScript
     - TypeScript
   category: e2e-testing
   ---
   ```

3. **Keep SKILL.md under 500 lines** — move detailed content to `reference/playbook.md`.

4. **Run validation** before submitting:
   ```bash
   python3 scripts/validate_skills.py
   ```

5. **Submit a Pull Request** with a clear description.

## Skill Structure Best Practices

- **SKILL.md**: Core workflow, decision trees, quick-reference patterns. Think "table of contents".
- **reference/playbook.md**: Complete code examples, debugging tables, CI/CD configs, best practices.
- **reference/advanced-patterns.md**: Advanced use cases, cloud integration, multi-language patterns.

## Quality Standards

- All code examples must be syntactically correct and runnable
- Include both local and cloud (LambdaTest) execution paths where applicable
- Add a debugging table with at least 10 common problems
- Include CI/CD integration (GitHub Actions preferred)
- Add a best practices checklist

## Code of Conduct

Be respectful, constructive, and inclusive. We're building tools to help the testing community.
