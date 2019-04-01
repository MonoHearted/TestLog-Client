from setuptools import setup, find_packages
from package import Package

setup(
	name='NGLMClient',
	version='1.0',
	description='Clientside for NGLogman.',
	url='https://git.genesyslab.com/ivorchen/NGLMClient',
	author='Bryan Niu / Ivor Chen',
	author_email='ivor.chen@genesys.com',
	packages=find_packages(),
	cmdclass={
		"package": Package
	}
)