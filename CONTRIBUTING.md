# Contribution guidelines

Contributions are welcome! Here are some guidelines to help you get started.

## Support the project

If you like this project and want to support it, you can:

- Give it a star on GitHub.
- Share it with others.
- Report issues or request new features.
- Contribute code, documentation, or tests.
- Sponsor the project on GitHub.


## Reporting issues

If you find a bug or have a feature request, please open an issue. Make sure to include a detailed description of the issue or feature request, and include any relevant information that can help us reproduce the issue.


## Contributing code

### Setup development environment

If you are using Visual Studio Code, you can use the included devcontainer in order to quickly set up a proper development environment.

### Discuss your changes

If you are planning to make a significant change, it is a good idea to discuss it first with the project authors. You can open an issue to discuss your changes or discuss it with other contributors the project's discussion channels.

### Implement your changes

Make your changes in a new git branch. Make sure to add tests for your changes.

### Run the tests and checks

In order for your changes to be accepted, they must pass all the tests and checks. We are using `nox` to run the tests and checks.
The tests and checks are defined in the [noxfile.py](noxfile.py) file.

You can run `nox` locally to run the tests and checks:

```shell
nox
```

### Add yourself to the contributors list

If you want to get credit from your contribution, add yourself to the following files:

- [pyproject.toml](pyproject.toml)
- [CITATION.cff](CITATION.cff)

### Create a pull request

Once you are happy with your changes, create a pull request. Make sure to include a description of your changes and why they are needed.

### Review process

Your pull request will be reviewed by the project maintainers. They may ask for changes or suggest improvements. Once your pull request is approved, it will be merged into the main branch.

