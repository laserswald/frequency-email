from distutils.core import setup
import py2exe


setup(
	name = "Frequency",
	version = "0.1",
	windows = [
		{
			"script": "src/frequency.py",
			"icon_resources": [(1, "src/icons/Frequency.ico")]
		}
	],
	script_args = ["py2exe"],
)
