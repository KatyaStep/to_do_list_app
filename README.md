# to_do_list_app
***
The to_do_list_app is an application that allows users to keep track of tasks that they plan to do.

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [How to use the project](#how-to-use-the-project)
5. [Tests for the app](#tests-for-the-app)

### General Info
***
The app has the following functionality:
- add a new task
- edit a task:  
    - set up a due date 
    - add some notes 
    - add a tag (not implemented yet)
- complete a task
- delete a task

### Technologies
***
A list of technologies used within the project:
* [Python]: Version 3.9.9
* [PyQt5]:  Version 5.15.6
* [sqlite]: Version 3.34.1
* [pytest]: Version 7.1.1

### Installation
***
A little intro about the installation.
````
$ git clone https://github.com/KatyaStep/to_do_list_app
$ cd ../path/to/the/requirements.txt file
$ activate your virtualenv
$ pip3 install -r requirements.txt

Note: if you want to manage db with GUI then you need to
      install DB Browser [https://sqlitebrowser.org]
````
### How to use the project
***
### Tests for the app
***
*  Tests are located in the folder [tests]
*  There are 3 files in the folder:
   * [conftest.py] : contains setttings for pytest and parsing command line arguments
   * [mock_model.py]: mocking db. Instead of db tests are working with dictionary.
   * [test_view.py]: file contains test cases. 
* To start tests you need to type in the terminal the following command:
````
$ python3 -m pytest --test_config tests/test_view.py

Note: --test_config is an argument that lets test environment know that we run tests. 
````