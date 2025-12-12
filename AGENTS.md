# AGENTS.md - AI Agent Guide for Learn OpenUSD Repository

This guide provides AI agents with comprehensive information on how to work with the Learn OpenUSD repository. Whether creating new content, reviewing changes, running tests, or using this repository as a knowledge base for OpenUSD questions, this document will help you navigate and contribute effectively.

## Repository Overview

**Learn OpenUSD** is an open-source documentation website that provides a complete learning path for OpenUSD (Universal Scene Description) development. The repository prepares developers for the OpenUSD Development Certification.

### Key Information
- **Purpose**: Educational documentation for OpenUSD with interactive examples
- **Tech Stack**: 
  - Sphinx (documentation generator)
  - MyST-NB (Jupyter notebooks as Markdown)
  - Python with OpenUSD (usd-core)
  - Git LFS (for images, videos, USD files)
- **Package Manager**: uv (for dependency management)
- **License**: Apache 2.0
- **Website**: https://docs.nvidia.com/learn-openusd/latest/index.html

## Quick Start Commands

### Building the Documentation

```bash
# Build HTML documentation
uv run sphinx-build -M html docs/ docs/_build/

# Clean build (remove cached outputs)
rm -rf docs/_build/

# Serve locally for preview
uv run python -m http.server 8000 -d docs/_build/html/
# Then open http://localhost:8000 in a browser
```

### Important Notes
- The build must complete without new Sphinx warnings or errors. There are 163 warnings in a typical build that are acceptable.
- The repository uses Git LFS for large files (images, videos, USD assets)
- Python 3.12+ is required (specified in `pyproject.toml`)

## Repository Structure

### Main Directories

```
LearnOpenUSD/
├── docs/                          # Main documentation source
│   ├── stage-setting/             # Module: USD fundamentals
│   ├── scene-description-blueprints/  # Module: Basic USD scene elements
│   ├── composition-basics/        # Module: Introduction to composition
│   ├── beyond-basics/             # Module: Advanced USD concepts
│   ├── creating-composition-arcs/ # Module: Deep dive into composition
│   ├── asset-structure/           # Module: Asset organization and composition patterns
│   ├── asset-modularity-instancing/ # Module: Instancing techniques
│   ├── data-exchange/             # Module: Import/export workflows
│   ├── what-openusd/              # Introduction to OpenUSD
│   ├── exercise_content/          # USD files and Python scripts for exercises
│   │   ├── foundations/
│   │   ├── composition_arcs/
│   │   ├── asset_structure/
│   │   ├── instancing/
│   │   └── data_exchange/
│   ├── images/                    # Screenshots, videos, GIFs by topic
│   ├── _assets/                   # Lesson-specific assets (within modules)
│   ├── _static/                   # Custom CSS, JavaScript
│   ├── _includes/                 # Reusable content snippets
│   ├── _templates/                # Custom Sphinx templates
│   ├── glossary.md                # OpenUSD terminology definitions
│   ├── index.md                   # Homepage
│   └── conf.py                    # Sphinx configuration
├── src/                           # Custom Python utilities
│   ├── directives.py              # Custom Sphinx directives (e.g., Kaltura)
│   └── utils/                     # Helper functions
├── pyproject.toml                 # Project dependencies
├── requirements.txt               # Locked dependencies
├── README.md                      # User-facing documentation
├── CONTRIBUTING.md                # Contribution guidelines
├── STYLEGUIDE.md                  # Documentation and coding guidelines
└── AGENTS.md                      # This file
```

## Content Structure and Conventions

### Style Guide

For detailed formatting conventions, MyST Markdown syntax, and writing guidelines, see **[STYLEGUIDE.md](STYLEGUIDE.md)**.

Key points:
- All documentation uses **MyST Markdown** (Markedly Structured Text)
- USD terminology should be **lowercase** unless at the start of a sentence (e.g., "prim" not "Prim")
- Correct spelling for all USD terms is defined in `docs/glossary.md`
- Link glossary terms on first use with the `{term}` role
- Files with executable Python code use **Jupytext** frontmatter

### File Organization

- **Images**: Place in `docs/images/<module-name>/` (PNG, JPG, GIF, WEBM, MP4)
- **Exercise files**: Store in `docs/exercise_content/<module-name>/`
- **Lesson assets**: Create `_assets/` subdirectories within lesson folders for build-time lesson assets.
- ZIP files are auto-generated during build from `exercise_content/` subdirectories

## Creating New Content

### Adding a New Lesson to an Existing Module

1. **Create the Markdown file** in the appropriate module directory (e.g., `docs/stage-setting/new-lesson.md`)
2. **Add the license header to files with executable code**
3. **Write the content** using MyST Markdown with appropriate directives
4. **Add to the module's index** by editing the `index.md` toctree in that module
5. **Add images** to `docs/images/<module-name>/`
6. **Test the build** to ensure no errors

### Creating a New Module

1. **Create the module directory** in `docs/` (e.g., `docs/my-new-module/`)
2. **Create an `index.md`** file as the module landing page
3. **Add subdirectories** for lessons if needed
4. **Create `setup.md`** if the module requires exercise files
5. **Add the module** to the main `docs/index.md` toctree
6. **Create exercise content** in `docs/exercise_content/my_new_module/`
7. **Add images** in `docs/images/my-new-module/`

## Reviewing Content and Providing Feedback

When reviewing changes or new content, evaluate these dimensions:

### Content Clarity
- [ ] Explanations are clear and accessible to learners
- [ ] Concepts progress logically from simple to complex
- [ ] Learning objectives are stated upfront
- [ ] Key takeaways summarize main points
- [ ] Technical jargon is explained or linked to glossary
- [ ] Examples are well-motivated with clear purpose

### Code Quality
- [ ] Python examples follow PEP 8 style guidelines
- [ ] Code is well-commented with explanatory comments
- [ ] Variable names are descriptive and meaningful
- [ ] Imports are included and correct
- [ ] Code executes without errors
- [ ] Examples are minimal and focused
- [ ] Output is printed when helpful for learning

### Consistency
- [ ] Files containing executable code include required Apache 2.0 license header
- [ ] Heading hierarchy is correct (single H1, proper nesting)
- [ ] MyST directives follow existing patterns
- [ ] Glossary terms are linked on first use
- [ ] Image paths follow convention (`../images/<module>/`)
- [ ] Code cell formatting matches existing lessons
- [ ] Tone and style match other lessons

### Technical Accuracy
- [ ] OpenUSD concepts are correctly explained
- [ ] API usage follows OpenUSD best practices
- [ ] Code examples produce expected results
- [ ] Glossary definitions are accurate
- [ ] Cross-references are correct
- [ ] Links to external docs are valid and relevant

### Structure and Navigation
- [ ] Lesson is added to appropriate toctree
- [ ] Cross-references use proper Sphinx syntax
- [ ] Glossary terms exist and are spelled correctly
- [ ] Module index is updated if needed
- [ ] Related lessons are linked
- [ ] Further reading links are provided

### Build Validation
- [ ] Build completes without warnings
- [ ] Build completes without errors
- [ ] No broken links or references
- [ ] All code cells execute successfully
- [ ] Images render correctly
- [ ] Videos embed properly

### Accessibility and Usability
- [ ] Images have descriptive alt text or captions
- [ ] Videos have accompanying descriptions
- [ ] Code examples have sufficient context
- [ ] Complex diagrams are explained in text
- [ ] Setup instructions are clear
- [ ] Prerequisites are stated

### Providing Constructive Feedback

When suggesting improvements:

1. **Be specific**: Point to exact lines or sections
2. **Explain why**: Clarify the issue or potential confusion
3. **Suggest alternatives**: Offer concrete improvements
4. **Reference examples**: Link to similar content done well
5. **Prioritize**: Distinguish must-fix from nice-to-have
