#-------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file checks for dependency deficits
#
# Author:        Konstantinos Konstantinidis
# email:         konkonst@iti.gr
# Created:       09/12/2016
# Copyright:     (c) ITI (CERTH) 2016
# Licence:       <apache licence 2.0>
#-------------------------------------------------------------------------------
import subprocess, platform
print('Running dependency checks...')
try:
    from setuptools import setup
except:   
    subprocess.call('python ez_setup.py')
    pass    
subprocess.call('easy_install -U pip')
if platform.architecture()[0] == '64bit':
    extension = 'win_amd64'
else:
    extension = 'win32'
subprocess.call('pip install numpy-1.11.2+mkl-cp35-cp35m-'+extension+'.whl')
subprocess.call('pip install matplotlib-1.5.3-cp35-cp35m-'+extension+'.whl')
subprocess.call('pip install scipy-0.18.1-cp35-cp35m-'+extension+'.whl')
subprocess.call('pip install pandas-0.19.1-cp35-cp35m-'+extension+'.whl')
setup(
    name="somocluGUI",
    description='somoclu GUI wrapper for the PERICLES project',
    author='Konstantinos Konstantinidis',
    author_email='konkonst@iti.gr',
    version='1.0',
    install_requires=('pip','somoclu','seaborn','sklearn')
)
