# MGO Health Checker

## Table of Contents

- [Purpose](#purpose)
- [Features](#features)
- [Usage](#usage)
  - [Adding the dependency](#adding-the-dependency)
  - [Bootstrapping the package](#bootstrapping-the-package)
- [Local development](#local-development)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Code quality](#code-quality)

## Purpose

When we were adding the same health check logic for the nth time in yet another
Python application, we realised this is a good candidate for a reusable package.
Not only can the logic for rendering the result in the browser be generic, also
the logic for checking each components health is always the same.

With this package, it is as easy as configuring which health checks you want for
your application and you're done. When the need arises for a new health checker,
it can be created here once and used by all.

## Features

- It provides an `APIRouter` to be registered by the implementing application
  built on FastAPI.
- It provides a library of health checkers to choose from. Simply add the ones
  you require to the collection and they will be included in the health status
  result.

## Usage

Follow the guide below to add this package to your own application.

> [!NOTE]
> At this point, the package is plug-n-play for FastAPI applications. It
> exposes a factory method for a `APIRouter` you can wire into your FastAPI app.
> You could in theory use the individual health checkers directly. This would
> require some custom code to print the health check result in a browser.

### Adding the dependency

Using the package manager of your choice (for example `uv`), install the
package. In this stage, the package is only availabe as a private MinVWS
repository, so you require read access to this repository to be able to install
it.

```bash
uv add "mgo-healthchecker[all] @ git+ssh://git@github.com/minvws/nl-mgo-package-healthchecker-private.git"
```

Since this package contains a evolving library of health checkers, it will
increasingly be the case that you don't require all of them, nor their
underlying packages.

To accommodate this, these dependencies are made optional, so you can choose
which ones you need and only install those libraries (in fact, most likely the
application already has these libraries installed).

The example below demonstrates how to include only the Redis health checker:

```bash
uv add "mgo-healthchecker[redis] @ git+ssh://git@github.com/minvws/nl-mgo-package-healthchecker-private.git"
```

### Bootstrapping the package

This packages exposes a factory method for creating the `APIRouter` that will
render the health check result. Import from
`mgo_healthchecker.routers.create_router`.

The route operation method uses FastAPI's `Depends` to invoke a callable
providing an instance of `HealthCheckCollection`. This collection is a simple,
typed list containing instances of the `HealthChecker` interface.

You are free to use your own dependency injection library for providing this
collection, as long as it is wrapped in a callable that `Depends` can invoke.

The following example shows a possible implementation using inject.py as DI
library:

```python
import inject
from fastapi import FastAPI
from mgo_healthchecker.routers import create_router
from mgo_healthchecker.utils import HealthCheckerCollection


def resolve_health_checker_collection() -> HealthCheckerCollection:
    return inject.instance(HealthCheckerCollection)


def run() -> FastAPI:
    app = FastAPI(title=acme)

    healthcheck_router = create_router(resolve_health_checker_collection)

    app.include_router(healthcheck_router)
```

Once the health check router is included in the FastAPI app, open
http://yourapp/health to view the health status of your app and its components.

## Local development

### Prerequisites

Please install the below programs if not present:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/)

### Setup

You can either open a Devcontainer workspace or start the Docker container and
open a shell.

For the latter, use the following Make commands:

```bash
make run
make shell
```

### Code quality

From within the `package` Docker container, there are a couple of Make commands
available to execute code quality tools that are also run of the CI.

To run and/or auto-fix them all sequentially, use one or both of the Make
commands below:

```bash
make check
make fix
```
