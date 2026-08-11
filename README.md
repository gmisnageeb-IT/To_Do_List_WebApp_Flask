To-do list web App - using Python and Flask framework
---------------------------------------------------------
Published website: https://nageebyrs.pythonanywhere.com/

Instructions to create an environment on VS Code
----------------------------------------------------------------
Run the terminal in your project folder:
1-Create the environment:
  python -m venv env
2-Activate the environment:
  c:\user\project-folder\ env/Scripts/activate
or
  c:\user\project-folder\ .\env\Scripts\activate

3- To upgrade pip inside your environment
(env) c:\user\project-folder\ python -m pip install --upgrade pip

Now you can install the libraries for your project in this environment

To copy the current env (to run on another computer)
--------------------------------------------------------
To install the libraries of the current environment to another one:
	A- freeze all pip  by:
		(env1) c:\user\project-folder\ pip freeze
	B-Copy the library into a text file:
		(env1) c:\user\project-folder\pip freeze > requirements.txt
  C-Go to another computer and copy the requirements.txt file inside your project folder
	   (env2) c:\user\project-folder\python -m pip install -r requirements.txt

To move from one environment to another, you must deactivate the current one
-----------------------------------------------------------------------
	(env) c:\user\project-folder\deactivate


To show all installed libraries in the current environment
---------------------------------------------------------------
pip list


In case activation does not work because of system policy
--------------------------------------------------------------
Write these two commands in the terminal

Get-ExecutionPolicy
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force


To find the path of Python 
----------------------------------
In CMD type:
where python

To know the version of Python
-----------------------------------
python --version



For the Flask library  (Note:Flask-Scss just for syling - not important , you can use CSS insted)
----------------------------------------------------------------------------------------------------
pip install Flask Flask-Scss Flask-SQLAlchemy

for styling the HTML in VS Code
---------------------------------------
extension needed to compile Scss style file :
1-Sass
2- Live Sass Compiler

Run the Flask web app in a web browser:
----------------------------------------
http://127.0.0.1:5000


Steps to deploy the project in PythonAnywhere
-------------------------------------
Go to this website: https://www.pythonanywhere.com/
Create an account, then :
Go to dashboard>consoles

Section 1:Download the project files 
-----------------------------------------
1- bash command
mkvirtualenv myvirtualenv --python=python3.13

2-(myinvetonment)  git clone
3- go inside your environment (project name)
	(myinvetonment) cd To_Do_List_WebApp_Flask
4- install the libraries in your environment
	pip install -r requirement.txt

section2: Connect the website with your project
----------------------------------------------
5- Go to the dashboard> Files
   Copy the path of your project name (To_Do_List_WebApp_Flask)
6- Go to the dashboard> Web
   Paste the path under sode section/source code section
	ex:/home/Nageebyrs/To_Do_List_WebApp_Flask

7-go to the dashboard >web
Under the source code, click on Configure WSGI configuration file and :
You will see a file like this (WSGI configuration file); open it
ex: /var/www/nageebyrs_pythonanywhere_com_wsgi.py
	A-delete all content

	B- add this code inside the  WSGI configuration file:

import sys
path ='/path/to/your/source/code'
if path not in sys.path:
	sys.path.append(path)
from app import app as application

then save

8- go to dashboard>files
   click on your project name() then copy the path 
9- go to dashboard>web
   Configure the WSGI configuration file  again and replace the path in the code with the correct one:

path ='/home/Nageebyrs/To_Do_List_WebApp_Flask'

then save

10- go to dashboard>files
    Copy the path of your environment folder
	ex: /home/Nageebyrs/.virtualenvs/myvirtualenv
11- go to dashboard under Virtualenv
	and paste the path of your environment
	ex: /home/Nageebyrs/.virtualenvs/myvirtualenv


12- go to dashboard under Reload section
    Click on the button:
	Reload your-website 
	ex: Nageebyrs.pythonanywhere.com

