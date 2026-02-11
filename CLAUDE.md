# CLAUDE.md

This file provides guidance for AI assistants working with the **superap** repository.

## Repository Overview

- **Repository**: `griulf-ai/superap`
- **Status**: New project — this repository was initialized without any source code, configuration, or documentation beyond this file.

## Project Structure

```
superap/
├── CLAUDE.md          # AI assistant guidance (this file)
└── .git/              # Git repository metadata
```

This is a greenfield project. As the codebase grows, update this section to reflect the actual directory structure, entry points, and module organization.

## Development Setup

No build system, package manager, or runtime dependencies have been configured yet. When they are added, document:

- Language and runtime version requirements
- Package manager and install commands
- Environment variables and secrets (without values)
- Local development server commands

## Common Commands

_To be populated as the project takes shape._ Example sections to add:

```
# Install dependencies
<command>

# Run development server
<command>

# Run tests
<command>

# Lint / format
<command>

# Build for production
<command>
```

## Code Conventions

When establishing conventions for this project, document them here. Recommended topics:

- **Language & framework** chosen for the project
- **Formatting** tool and config (e.g., Prettier, Black, rustfmt)
- **Linting** tool and config (e.g., ESLint, Ruff, Clippy)
- **Naming conventions** (files, variables, functions, components)
- **Import ordering** rules
- **Error handling** patterns
- **Testing** framework and conventions (unit, integration, e2e)

## Architecture

_To be documented once the project architecture is defined._ Include:

- High-level architecture diagram or description
- Key modules and their responsibilities
- Data flow patterns
- API design conventions
- Database schema or ORM patterns

## Git Workflow

- **Default branch**: to be established (typically `main`)
- Write clear, concise commit messages focused on _why_ rather than _what_
- Keep pull requests focused on a single concern
- Ensure all checks pass before merging

## Guidelines for AI Assistants

1. **Read before writing** — always read existing files before proposing changes.
2. **Minimal changes** — only make changes that are directly requested or clearly necessary.
3. **No over-engineering** — avoid adding features, abstractions, or configurability beyond what is asked.
4. **Security awareness** — do not introduce command injection, XSS, SQL injection, or other OWASP top-10 vulnerabilities.
5. **Keep this file current** — update CLAUDE.md whenever significant project structure, tooling, or conventions change.
