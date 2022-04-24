# How to contribute

Feel free to:

- [Create an issue](https://help.github.com/articles/creating-an-issue/)
- [Make a pull request](https://services.github.com/on-demand/github-cli/open-pull-request-github) into the `main` branch

Here is how you can help, a lot of steps are related to GitHub, not specifically our roles.

## 1. Create an issue

When you see some issue or have an idea for improvement, [create an issue](https://github.com/lablabs/ansible-role-rke2/issues).

## 2. Fork the project

Click on `fork` on the top-right corner and fork the repository.

## 3. Make the changes

Do the changes in your own GitHub namespace.

## 4. Test the changes

Install [molecule](https://molecule.readthedocs.io/en/stable/) and run the test:

```bash
pip install molecule molecule-docker ansible-lint docker
cd ansible-github_actions_runner

# Test of single node RKE2 deployment
molecule test

# Test of 2 node cluster (one server, one agent)
molecule test --scenario-name cluster

# Test of 4 node cluster (3 tained server nodes in HA, one agent)
molecule test --scenario-name ha_cluster
```

## 5. Create a pull request

Please create a pull request into the `main` branch. Here is [how to do it](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork).
