from setuptools import setup, find_packages

setup(
<<<<<<< .mine
	name = "Frequency",
	version = "0.1",
	description = "An email program written in Python.",	
	
	windows = [
		{
			"script": "frequency.py",
			"icon_resources": [(1, "icons/Frequency.ico")]
		}
	],
	script_args = ["py2exe"],
	options = {
		'py2exe':{
				"dist_dir" : "../dist/"
		}
	},
	data_files=[ ("icons",["icons/Frequency.ico", 
						   "icons/email.png", 
						   "icons/email_add.png",
						   "icons/email_delete.png",
						   'icons/email_attach.png',
						   'icons/email_edit.png',
						   'icons/door_in.png',
						   'icons/user.png',
						   'icons/wrench.png'])]
=======
    name = "Frequency",
    version = "0.1",
    packages = find_packages(),
>>>>>>> .r10
)
