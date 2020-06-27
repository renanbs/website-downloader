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

- Tests will run with coverage minimum at 70%.

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
(website_donwloader-3.8.3) ➜  website-downloader git:(master) ✗ make test
# "Running unit tests"
pytest -v --cov-report=term-missing --cov-report=html --cov-report=xml --cov=website_downloader --cov-fail-under=70
Test session starts (platform: linux, Python 3.8.3, pytest 5.4.3, pytest-sugar 0.9.3)
rootdir: /home/renan/src/website-downloader, inifile: setup.cfg
plugins: mock-3.1.1, requests-mock-1.8.0, sugar-0.9.3, cov-2.10.0, lazy-fixture-0.6.3
collecting ... 
 website_downloader/services/tests/test_html.py ✓✓                                                                                                                                                                                                         40% ████      
 website_downloader/services/tests/test_image.py ✓✓✓                                                                                                                                                                                                      100% ██████████

----------- coverage: platform linux, python 3.8.3-final-0 -----------
Name                                              Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------
website_downloader/__init__.py                        0      0   100%
website_downloader/conftest.py                        9      0   100%
website_downloader/services/__init__.py               0      0   100%
website_downloader/services/dir.py                   15     15     0%   1-21
website_downloader/services/exception.py              2      0   100%
website_downloader/services/html.py                   9      0   100%
website_downloader/services/image.py                 41      1    98%   45
website_downloader/services/tests/__init__.py         0      0   100%
website_downloader/services/tests/test_html.py       23      0   100%
website_downloader/services/tests/test_image.py      71      0   100%
website_downloader/services/utils.py                  8      3    62%   9-11
website_downloader/wb_downloader.py                  30     30     0%   1-54
-------------------------------------------------------------------------------
TOTAL                                               208     49    76%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml

Required test coverage of 70% reached. Total coverage: 76.44%

Results (0.42s):
       5 passed
```

---

#### Coverage not reached
```zsh
(website_donwloader-3.8.3) ➜  website-downloader git:(master) ✗ make test
# "Running unit tests"
pytest -v --cov-report=term-missing --cov-report=html --cov-report=xml --cov=website_downloader --cov-fail-under=80
Test session starts (platform: linux, Python 3.8.3, pytest 5.4.3, pytest-sugar 0.9.3)
rootdir: /home/renan/src/website-downloader, inifile: setup.cfg
plugins: mock-3.1.1, requests-mock-1.8.0, sugar-0.9.3, cov-2.10.0, lazy-fixture-0.6.3
collecting ... 
 website_downloader/services/tests/test_html.py ✓✓                                                                                                                                                                                                         40% ████      
 website_downloader/services/tests/test_image.py ✓✓✓                                                                                                                                                                                                      100% ██████████

----------- coverage: platform linux, python 3.8.3-final-0 -----------
Name                                              Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------
website_downloader/__init__.py                        0      0   100%
website_downloader/conftest.py                        9      0   100%
website_downloader/services/__init__.py               0      0   100%
website_downloader/services/dir.py                   15     15     0%   1-21
website_downloader/services/exception.py              2      0   100%
website_downloader/services/html.py                   9      0   100%
website_downloader/services/image.py                 41      1    98%   45
website_downloader/services/tests/__init__.py         0      0   100%
website_downloader/services/tests/test_html.py       23      0   100%
website_downloader/services/tests/test_image.py      71      0   100%
website_downloader/services/utils.py                  8      3    62%   9-11
website_downloader/wb_downloader.py                  30     30     0%   1-54
-------------------------------------------------------------------------------
TOTAL                                               208     49    76%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml

FAIL Required test coverage of 80% not reached. Total coverage: 76.44%

Results (0.43s):
       5 passed
make: *** [Makefile:59: test] Error 1
(website_donwloader-3.8.3) ➜  website-downloader git:(master) ✗

``` 

---

#### Test failed

```zsh
(website_donwloader-3.8.3) ➜  website-downloader git:(master) ✗ make test
# "Running unit tests"
pytest -v --cov-report=term-missing --cov-report=html --cov-report=xml --cov=website_downloader --cov-fail-under=70
Test session starts (platform: linux, Python 3.8.3, pytest 5.4.3, pytest-sugar 0.9.3)
rootdir: /home/renan/src/website-downloader, inifile: setup.cfg
plugins: mock-3.1.1, requests-mock-1.8.0, sugar-0.9.3, cov-2.10.0, lazy-fixture-0.6.3
collecting ... 

―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――― test_should_download_index_html ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

requests_mock = <requests_mock.mocker.Mocker object at 0x7fcfd51c48b0>, tmp_path = PosixPath('/tmp/pytest-of-renan/pytest-42/test_should_download_index_htm0')

    def test_should_download_index_html(requests_mock, tmp_path):
        url = 'http://xyz.com'
        content = 'just the content'
        requests_mock.get(url, status_code=200, text=content)
    
        with patch('website_downloader.services.html.open', mock_open()) as mocked_file:
            result = download_page(url, tmp_path)
    
            mocked_file.assert_called_once_with(os.path.join(str(tmp_path.absolute()), 'index.html'), 'w')
    
            mocked_file().write.assert_called_once_with(content)
>           assert content != result
E           AssertionError: assert 'just the content' != 'just the content'

website_downloader/services/tests/test_html.py:21: AssertionError

 website_downloader/services/tests/test_html.py ⨯✓                                                                                                                                                                                                         40% ████      
 website_downloader/services/tests/test_image.py ✓✓✓                                                                                                                                                                                                      100% ██████████

----------- coverage: platform linux, python 3.8.3-final-0 -----------
Name                                              Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------
website_downloader/__init__.py                        0      0   100%
website_downloader/conftest.py                        9      0   100%
website_downloader/services/__init__.py               0      0   100%
website_downloader/services/dir.py                   15     15     0%   1-21
website_downloader/services/exception.py              2      0   100%
website_downloader/services/html.py                   9      0   100%
website_downloader/services/image.py                 41      1    98%   45
website_downloader/services/tests/__init__.py         0      0   100%
website_downloader/services/tests/test_html.py       23      0   100%
website_downloader/services/tests/test_image.py      71      0   100%
website_downloader/services/utils.py                  8      3    62%   9-11
website_downloader/wb_downloader.py                  30     30     0%   1-54
-------------------------------------------------------------------------------
TOTAL                                               208     49    76%
Coverage HTML written to dir htmlcov
Coverage XML written to file coverage.xml

Required test coverage of 70% reached. Total coverage: 76.44%
======================================================================================================================== short test summary info ========================================================================================================================
FAILED website_downloader/services/tests/test_html.py::test_should_download_index_html - AssertionError: assert 'just the content' != 'just the content'

Results (0.44s):
       4 passed
       1 failed
         - website_downloader/services/tests/test_html.py:10 test_should_download_index_html
make: *** [Makefile:59: test] Error 1
(website_donwloader-3.8.3) ➜  website-downloader git:(master) ✗
```


## How to use this project

### TODO
