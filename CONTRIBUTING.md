
## OpenUSD Code Samples OSS Contribution Rules

#### Issue Tracking

* All enhancement, bugfix, or change requests must begin with the creation of a [OpenUSD Code Samples Issue Request](https://github.com/NVIDIA-Omniverse/OpenUSD-Code-Samples/issues).
  * The issue request must be reviewed by OpenUSD Code Samples engineers and approved prior to code review.


#### Coding Guidelines

- All source code contributions must strictly adhere to the [OpenUSD Code Samples Guidelines](CODE-SAMPLE-GUIDELINES.md).

- In addition, please follow the existing conventions in the relevant file, submodule, module, and project when you add new code or when you extend/fix existing functionality.

- Avoid introducing unnecessary complexity into existing code so that maintainability and readability are preserved.

- All development should happen against the "main" branch of the repository. Please make sure the base branch of your pull request is set to the "main" branch when filing your pull request.

- Try to keep pull requests (PRs) as concise as possible:
  - Avoid committing commented-out code.
  - Wherever possible, each PR should address a single concern. If there are several otherwise-unrelated things that should be fixed to reach a desired endpoint, our recommendation is to open several PRs and indicate the dependencies in the description. The more complex the changes are in a single PR, the more time it will take to review those changes.

- Write commit titles using imperative mood and [these rules](https://chris.beams.io/posts/git-commit/), and reference the Issue number that is being addressed. Following is the recommended format for commit texts:
```
<Commit Title>

<Commit Body>
```

- Ensure that the Sphinx build log is clean, meaning no warnings or errors should be present.

- Ensure that all code blocks execute correctly prior to submitting your code.

- All OSS components must contain accompanying documentation (READMEs) describing the functionality, dependencies, and known issues.

  - See `README.md` for existing samples and plugins for reference.

- All OSS components must have an accompanying test.

  - If introducing a new component, such as a plugin, provide a test sample to verify the functionality.

- Make sure that you can contribute your work to open source (no license and/or patent conflict is introduced by your code). You will need to [`sign-off`](#signing-your-work) your commit.

- Thanks in advance for your patience as we review your contributions; we do appreciate them!


#### Pull Requests
Developer workflow for code contributions is as follows:

1. Developers must first [fork](https://help.github.com/en/articles/fork-a-repo) the [upstream](https://github.com/NVIDIA-Omniverse/OpenUSD-Code-Samples) OpenUSD Code Samples repository.

2. Git clone the forked repository.
  ```bash
git clone https://github.com/YOUR_USERNAME/YOUR_FORK.git OpenUSD-Code-Samples
  ```

3. Create a branch off of the "main" branch and commit changes. See [Coding Guidelines](#coding-guidelines) for commit formatting rules.

```bash
# Create a branch off of the "main" branch
git checkout -b <local-branch> <remote-branch>
git add <path-to-files>
# -s flag will "sign-off" on your commit, we require all contributors to sign-off on their commits. See below for more
git commit -s -m "<Commit Title>"
```

4. Push Changes to the personal fork.
  ```bash
# Push the commits to a branch on the fork (remote).  
git push -u origin <local-branch>:<remote-branch>
  ```

5. Please make sure that your pull requests are clean. Use the rebase and squash git facilities as needed to ensure that the pull request is as clean as possible.

6. Once the code changes are staged on the fork and ready for review, a [Pull Request](https://help.github.com/en/articles/about-pull-requests) (PR) can be [requested](https://help.github.com/en/articles/creating-a-pull-request) to merge the changes from your branch to the upstream "main" branch.
    * Exercise caution when selecting the source and target branches for the PR.
    * If you haven't included a link to the Issue you are addressing in your commit message, add it now to the PR description.
    * Creation of a PR creation kicks off the code review process.
    * At least one OpenUSD Code Samples engineer will be assigned for the review.
    * While under review, mark your PRs as work-in-progress by prefixing the PR title with [WIP].

7. Since there is no CI/CD process in place yet, the PR will be accepted and the corresponding issue closed only after adequate testing has been completed, manually, by the developer and/or OpenUSD Code Samples engineer reviewing the code.


#### Signing Your Work

* We require that all contributors "sign-off" on their commits. This certifies that the contribution is your original work, or you have rights to submit it under the same license, or a compatible license.

  * Any contribution which contains commits that are not Signed-Off will not be accepted.
  * Note that "sign-off" is not the same as a "signed commit". "Signed-off-by" is a tag that is included in a commit message, and can be done through `-s` or inserting the text at the bottom of a commit message manually (see below). The flag `-S` is for a "signed commit", which is cryptographically identifiable. For more information on the differences, see [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) and [About commit signoffs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-the-commit-signoff-policy-for-your-repository#about-commit-signoffs)

* To sign off on a commit you simply use the `--signoff` (or `-s`) option when committing your changes:
  ```bash
  $ git commit -s -m "Add cool feature."
  ```
  This will append the following to your commit message:
  ```
  Signed-off-by: Your Name <your@email.com>
  ```

* Full text of the DCO:

  ```
    Developer Certificate of Origin
    Version 1.1

    Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

    Everyone is permitted to copy and distribute verbatim copies of this
    license document, but changing it is not allowed.

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.
  ```