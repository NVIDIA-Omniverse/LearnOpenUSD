# Learn OpenUSD
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Learn OpenUSD is a full learning path to prepare developers for the OpenUSD Development Certification. This open source repository is open to contributions to improve the learning experience for everyone and so that teachers and trainers can take it and adapt it for their audiences.

## Configuration
This repository uses [uv](https://docs.astral.sh/uv/) for dependency management. If you're new to uv, you don't need to know much more than the commands we use in the [build instructions](#How-to-Build). We recommend [installing uv](https://docs.astral.sh/uv/getting-started/installation/).

## How to Build
1. `uv run sphinx-build -M html docs/source/ docs/build/`
1. `uv run python -m http.server 8000 -d docs/build/html/`
1. In a web browser, open `http://localhost:8000`

## Have an Idea for a New Example or new content?
Ideas for new content to can help other developers are always welcome. Please [create a new issue](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/issues) requesting a new code sample and put [New Request] at the end of your title. Someone from the NVIDIA team or OpenUSD community will pick it up. If you can contribute it yourself, even better!

## Find a Typo or an Error?
Please let us know if you find any mistakes or non-working code samples. [File an issue](https://github.com/NVIDIA-Omniverse/LearnOpenUSD/issues) with a comment that this is a bug.

## Contributing
Contributions are welcome! If you would like to contribute, please read our [Contributing Guidelines](./CONTRIBUTING.md) to understand how to contribute.