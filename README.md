# Learn OpenUSD
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[Learn OpenUSD](https://docs.nvidia.com/learn-openusd/latest/index.html) is a full learning path to prepare developers for the OpenUSD Development Certification. This open source repository is open to contributions to improve the learning experience for everyone and so that teachers and trainers can take it and adapt it for their audiences.

If you just want to access the learning content, visit the rendered [Learn OpenUSD website](https://docs.nvidia.com/learn-openusd/latest/index.html).

## Configuration

### uv
This repository uses [uv](https://docs.astral.sh/uv/) for dependency management. If you're new to uv, you don't need to know much more than the commands we use in the [build instructions](#How-to-Build). We recommend [installing uv](https://docs.astral.sh/uv/getting-started/installation/).

### Git LFS
This repository uses Git Large File Storage to store images, videos, and USD content. To ensure a frictionless process, make sure you have it installed before cloning the repository.

**Install:** 

*(You only need to do this once per machine)*
```
git lfs install
```

If you cloned this repo before installing LFS, you can download all LFS to properly configure your repo.

**Download LFS files:** 

*(You only need to do this once for this repo)* 
```
git lfs pull
```

## How to Build
1. `uv run sphinx-build -M html docs/ docs/_build/`
1. `uv run python -m http.server 8000 -d docs/_build/html/`
1. In a web browser, open `http://localhost:8000`

### Build System Details

The build process:
1. MyST-NB executes Python code cells
2. Sphinx processes directives and cross-references
3. Custom extensions copy assets and create exercise ZIPs
4. Glossary is extracted for interactive graph
5. HTML is generated with custom theme

## Have an Idea for a New Example or New Content?
Ideas for new content that can help other developers are always welcome. Please [create a new issue](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/issues) describing the type of new content you are requesting and put [New Request] at the end of your title. Someone from the NVIDIA team or OpenUSD community will pick it up. If you can contribute it yourself, even better!

## Find a Typo or an Error?
Please let us know if you find any mistakes or non-working examples or exercises. [File an issue](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/issues) with a comment that this is a bug.

## Contributing
Contributions are welcome! If you would like to contribute, please read our [Contributing Guidelines](./CONTRIBUTING.md) to understand how to contribute.