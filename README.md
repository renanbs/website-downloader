# Website Downloader


This project is a website downloader. The idea is to download the index.html, all images and scripts to have a fully loaded page.
This project install pytest as the testing framework.

 - This project was only tested on Linux.


## Requirements

 - Make
 - Python 3.8+


## Development Environment
 
 
### Automation tool

This project uses `Makefile` as automation tool.

### Set-up Virtual Environment

The following commands will install and set-up `pyenv` tool (https://github.com/pyenv/pyenv) used to create/manage virtual environments:

> Just replace `zshrc` with the configuration file of your interpreter, like `bashrc`

```bash
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.zshrc
$ exec "$SHELL"
$ git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
$ exec "$SHELL"
```

After that, access the project directory and execute `make create-venv` to create and recreate the virtual environment.

> The environment will be create in your home directory:

> `$PROJECT_NAME` and `$PYTHON_VERSION` are variables defined in the Makefile

```bash
$HOME/.pyenv/versions/$PROJECT_NAME-$PYTHON_VERSION/bin/python

/home/renan/.pyenv/versions/website_downloader-3.8.3/bin/python
```


### Run unit tests, style and convention

- Tests will run with coverage minimum at 90%.

Running code style
```bash
make code-convention
```
Running unit tests
```bash
make test
```
Running code style and all tests
```bash
make
```

## Examples of make outputs

#### All Tests passed, coverage and style are ok
```zsh
(my_project-3.8.3) ➜  python-project-template git:(master) ✗ make test
# "Running unit tests"
pytest -v --cov-report=term-missing --cov-report=html --cov-report=xml --cov=my_code --cov-fail-under=90
Test session starts (platform: linux, Python 3.8.0, pytest 5.4.1, pytest-sugar 0.9.3)
rootdir: /home/renan/src/python-project-template, inifile: setup.cfg
plugins: cov-2.8.1, sugar-0.9.3, lazy-fixture-0.6.3
collecting ... 
 my_code/tests/test_my_code_file.py ✓                                                                                                                                                                                                                     100% ██████████

----------- coverage: platform linux, python 3.8.0-final-0 -----------
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
my_code/__init__.py                      0      0   100%
my_code/my_code_file.py                  2      0   100%
my_code/tests/__init__.py                0      0   100%
my_code/tests/test_my_code_file.py       5      0   100%
------------------------------------------------------------------
TOTAL                                    7      0   100%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml

Required test coverage of 90% reached. Total coverage: 100.00%

Results (0.10s):
       1 passed
(my_project-3.8.0) ➜  python-project-template git:(master) ✗
```

---

#### Coverage not reached
```zsh
(my_project-3.8.0) ➜  python-project-template git:(master) ✗  make test

# "Running unit tests"
pytest -v --cov-report=term-missing --cov-report=html --cov-report=xml --cov=my_code --cov-fail-under=90
Test session starts (platform: linux, Python 3.8.0, pytest 5.4.1, pytest-sugar 0.9.3)
rootdir: /home/renan/src/python-project-template, inifile: setup.cfg
plugins: cov-2.8.1, sugar-0.9.3, lazy-fixture-0.6.3
collecting ... 

----------- coverage: platform linux, python 3.8.0-final-0 -----------
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
my_code/__init__.py                      0      0   100%
my_code/my_code_file.py                  2      2     0%   2-3
my_code/tests/__init__.py                0      0   100%
my_code/tests/test_my_code_file.py       0      0   100%
------------------------------------------------------------------
TOTAL                                    2      2     0%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml

FAIL Required test coverage of 90% not reached. Total coverage: 0.00%

Results (0.10s):
make: *** [Makefile:58: test] Error 1
(my_project-3.8.0) ➜  python-project-template git:(master) ✗ 

``` 

---

#### Test failed

```zsh
(my_project-3.8.0) ➜  python-project-template git:(master) ✗ make test                
# "Running unit tests"
pytest -v --cov-report=term-missing --cov-report=html --cov-report=xml --cov=my_code --cov-fail-under=90
Test session starts (platform: linux, Python 3.8.0, pytest 5.4.1, pytest-sugar 0.9.3)
rootdir: /home/renan/src/python-project-template, inifile: setup.cfg
plugins: cov-2.8.1, sugar-0.9.3, lazy-fixture-0.6.3
collecting ... 

―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――― test_just_a_example ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

    def test_just_a_example():
        value_1 = 2
        value_2 = 2
>       assert dumb_function(value_1, value_2) == 2
E       assert 4 == 2
E        +  where 4 = dumb_function(2, 2)

my_code/tests/test_my_code_file.py:7: AssertionError

 my_code/tests/test_my_code_file.py ⨯                                                                                                                                                                                                                     100% ██████████

----------- coverage: platform linux, python 3.8.0-final-0 -----------
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
my_code/__init__.py                      0      0   100%
my_code/my_code_file.py                  2      0   100%
my_code/tests/__init__.py                0      0   100%
my_code/tests/test_my_code_file.py       5      0   100%
------------------------------------------------------------------
TOTAL                                    7      0   100%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml

Required test coverage of 90% reached. Total coverage: 100.00%
======================================================================================================================== short test summary info ========================================================================================================================
FAILED my_code/tests/test_my_code_file.py::test_just_a_example - assert 4 == 2

Results (0.12s):
       1 failed
         - my_code/tests/test_my_code_file.py:4 test_just_a_example
make: *** [Makefile:58: test] Error 1
(my_project-3.8.0) ➜  python-project-template git:(master) ✗ 

```


## How to use it
