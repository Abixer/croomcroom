Steps to setup under windows.

1. Install python 3.3.3 for 64bit. 
	http://www.python.org/download/releases/3.3.3/
	
2. Run the following script from a command shell. This will require admin rights.
	https://raw.github.com/pypa/pip/master/contrib/get-pip.py
	
	Command :
	$ python get-pip.py
	

3. Add the scripts directory in your install folder to your path. Log off and log on.

4. Run the following command to install virtualenv

	Command :
	$ pip install virtualenv
	
5. Check out the project from bitbucket.
	
5. Navigate to the project root and activate the virtual env.

	Command :
	$ .\env\Scripts\activate
	
At any point, you can leave this environment by writing

	Command :
	(env) deactivate
	
7. Now you should be in the virtual env and can start development. I reccomend going through a django tutorial to figure things out,
the official one is good.

8. Before you run, be sure to install postgresql 9.3.2-3
(List of downloads)
http://www.postgresql.org/download/

(direct link)
http://get.enterprisedb.com/postgresql/postgresql-9.3.2-3-windows-x64.exe


Things of note :
-The database is not in github. Generate it on your own machine.


