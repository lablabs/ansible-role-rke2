# How to contribute

Feel free to:

- [Create an issue](https://help.github.com/articles/creating-an-issue/)
- [Make a pull request](https://services.github.com/on-demand/github-cli/open-pull-request-github) into the `main` branch

Here is how you can help, a lot of steps are related to GitHub, not specifically my roles.

## 1. Create an issue

When you see some issue or have an idea for improvement, [create an issue](https://github.com/lablabs/ansible-nexus_config/issues).

## 2. Fork the project

Click on `fork` on the top-right corner and fork the repository.

## 3. Install pre-commit

Install [Pre-commit](https://pre-commit.com/#install) software

## 4. Make the changes

Do the changes in your own GitHub namespace.

## 5. Test the changes

**Note:** I will test the role again, so you don't need to do that if you don't want to.

Install [molecule](https://molecule.readthedocs.io/en/stable/) and run the test:

```bash
pip install molecule molecule-docker ansible-lint docker
cd ansible-nexus_config
molecule test
```

> You will need to edit the files in `molecule/default` directory (please do not commit those changes)

## 6. Create a pull request

Please create a pull request into the `main` branch. Here is [how to do it](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork).

## 7. Semantic Commits

Commits must follow conventional specs below:

- `ci:` Changes to our CI configuration files and scripts (example scopes: GitHub Actions)
- `docs:` Documentation only changes
- `feat:` A new feature
- `fix:` A bug fix
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `style:` Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `test:` Adding missing tests or correcting existing tests
