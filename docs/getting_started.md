# 🚀 Getting Started

In this guide we'll walk you through setting up and using `BaSyx Python PoC`.

In general, you should have [VS Code](https://https://code.visualstudio.com/) installed (which is fully
supported by us). Alternatively you could also use any other python IDE (e.g. PyCharm), however then you're on
your own considering setup.

We provide a [dev container](https://code.visualstudio.com/docs/remote/containers) which is more frictionless
(because all dependencies are installed automatically in an isolated environment) than standard
__non container development__.

What is better for you comes down to your personal preferences. __BUT:__ using the devcontainer is the
recommended way.

There are some guidelines to contribute to this repository. Please read the
[contribution guidelines](../CONTRIBUTE.md) before you start.

!!! note

  This "Getting Started"-guide is for using this project (not development - if you want to develop
  please refer to the [Development Guide](./dev_guide.md)).

## Prerequisites

Please be sure to fulfill the following prerequisites.

    basyx-python-sdk
    typing>=3.7.4.3
    PyYAML>=6.0
    argparse>=1.4.0
    pydantic>=2.11.5
    requests>=2.32.3
    python-json-logger>=3.3.0
    pytest>=8.3.5
    pytest-cov>=6.1.1

All needed prerequisites are listed in the `requirements.txt' file and will be loaded with the DevContainer automatically.

!!! tip

  You can also look at the source code of this project for reference - especially the
  devcontainer (see `.devcontainer` directory in the repo) has everything set up already.

### Needed tooling

You should already have installed Docker. If it's not present on your system download and install it:

* [Docker](www.dockerhub.com)
* [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) in VS Code

## Using DevContainer

The `BaSyx Python PoC` provides a DevContainer stack, which contains the following containers:
* `Python`: container for developing
* `BaSyx Python SDK Server`: AAS HTTP server provided by the [eclipse basyx python SDK](https://github.com/eclipse-basyx/basyx-python-sdk/blob/main/server/README.md)
* `AASX-Server`: AASX Server based on code of AASX Package Explorer provided by [Admin-shell-IO AASX Server](https://hub.docker.com/r/adminshellio/aasx-server-blazor-for-demo)

Start DevContainer to start the container stack. After all containers are running, the `BaSyx Python SDK Server` is running on [localhost:8081](http://localhost:8081/)

## Developing in DevContainer

??? warning "if you're on Windows..."

  Be careful not to mount your Windows file system into wsl2 / the devcontainer because this will be slow as
  hell regarding file IO. This will be automatically the case if you clone your repo on a windows drive,
  open it in VS Code and then open the devcontainer. Instead, you can use one of the following approaches:

  - Clone your repo in wsl2 in the native wsl2 file system (not beginning with `/mnt` !!) and open it from
  there:
    [Open a wsl2 folder in a container on Windows](https://code.visualstudio.com/docs/remote/containers#_open-a-wsl-2-folder-in-a-container-on-windows)
  - Clone your repo directly in a new docker volume (which also happens to live in the wsl2 file system):
      [Open a git repository or GitHub pr in an isolated container volume](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-a-git-repository-or-github-pr-in-an-isolated-container-volume)

## Developing natively (Windows or Linux)

This is a little more work because you need to arrange prerequisites first:

- Python (see <https://python.org>) - recommended version: 3.13
- Tooling: we rely on many tools for linting, formatting, testing etc...
  There are a (beta) setup scripts available to install these at:

  - 🪟 Windows: `template/setup/setup.sh`
  - 🐧 Linux: `template\setup\setup.ps1`

  use them at your own risk and fix bugs if you encounter them.
  Even if you install the tools by hand these scripts might be a good starting point to see what you need.

## Usage

### in devcontainer - like it's intended

open VS Code by typing:

```shell
code
```

When VS Code opens you should see a notification asking you if you want to reload VS Code in
devcontainer - acknowledge it.
(If that's not working keep sure that you installed the
[remote container extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
in VS Code on your host).

### Native development (Windows, Linux, etc.) - without devcontainer

- Open the repo in VS Code
- __On first start:__ install poetry packages and pre-commit hooks with VS Code terminal (may take some time)

  ```shell
  # install poetry dependencies
  poetry install
  # install pre-commit hooks
  pre-commit install --install-hooks
  ```

- in VS Code select the python interpreter at `./.venv/bin/python` (created by poetry install command before) by
  - `Command Palette [F1] -> Python: Select Interpreter`
  - if the poetry virtual env created before isn't shown restart vscode and retry

## Usage / Development

- you can just hit F5 and should be able to run/debug into the code
