# Shopping Cart Unit Tests

This repository contains the example code for Chapter 5 in Andrew Knight's book, *The Way To Test Software*.
It contains a Python unit test example project named `shopping_cart` that tests code for a (fictitious) shopping cart.
The project shows how to write unit tests for callables and classes,
as well as how to fake dependencies with mocks and patches.

Even though this project's primary purpose is to provide example code for the book,
it can nevertheless be a general example for good Python unit testing practices.


## Installation

The example code should work on any operating system (Windows, macOS, Linux).
To install it:

1. Install [Python](https://www.python.org/) 3.8 or higher.
2. Clone this repository onto your local machine.
3. Install dependency packages from the command line:
   * Change directory to the project's root directory.
   * Run `pip install -r requirements.txt` to install all dependencies.


## Execution

To run the unit tests:

```
cd shopping_cart
python -m pytest tests
```

To run the tests with code coverage:

```
python -m pytest tests --cov=orders --cov-branch
```
