#!/usr/bin/env python
import os
import subprocess
import re

from setuptools import setup, find_packages

# Get the Quickstart documentation
with open('README.md') as readme:
    INSTALL = readme.read()

# Update version from latest git tags.
# Create a version file in the root directory
version_py = os.path.join(os.path.dirname(__file__), 'django_basin3d/version.py')
version_msg = "# Managed by setup.py via git tags.  **** DO NOT EDIT ****"
try:
    git_describe = subprocess.check_output(["git", "describe", "--tags"]).rstrip().decode('utf-8')

    with open(version_py, 'w') as f:
        f.write(version_msg + os.linesep + "__version__ = '" + git_describe.split("-")[0] + "'")
        f.write(os.linesep + "__release__ = '" + git_describe + "'" + os.linesep)

except Exception:
    # If there is an exception, this means that git is not available
    # We will used the existing version.py file
    if not os.path.exists(version_py):
        with open(version_py, 'w') as f:
            f.write(version_msg + os.linesep + "__version__='0'")
            f.write(os.linesep + "__release__='0'" + os.linesep)

__release__ = None
if os.path.exists(version_py):
    with open(version_py) as f:
        code = compile(f.read(), version_py, 'exec')
    exec(code)

# Get the requirements
dependency_links=[]
required = []
with open('requirements.txt') as f:
    for r in f.read().splitlines():
        if "github.com" in r:
            m = re.search(r"@(.*)#", r)
            if not m: continue
            version = m.group(1)
            m = re.search(r"=(.*)", r)
            if not m: continue
            name = m.group(1)
            required.append(f"{name} @ {r}")
            dependency_links.append(r)
        else:
            required.append(r)

setup(name='django-basin3d',
      version=__release__,
      description='Django Framework for Broker for Assimilation, Synthesis and Integration of eNvironmental Diverse, Distributed Datasets',
      long_description=INSTALL,
      author='Valerie Cork Hendrix',
      author_email='vchendrix@lbl.gov',
      packages=find_packages(exclude=["*.tests", ]),
      py_modules=['manage'],
      include_package_data=True,
      install_requires=required,
      dependency_links=dependency_links,
      python_requires='>=3.7,<3.9',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Django :: 3.0',
          'License :: OSI Approved :: BSD License',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: GIS',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ]
      )
