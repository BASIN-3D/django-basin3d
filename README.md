# django-basin3d
Django web framework for Broker for Assimilation, Synthesis and Integration of eNvironmental Diverse, Distributed Datasets



## Development Practices

* django-basin3d uses the [GitFlow model](https://datasift.github.io/gitflow/IntroducingGitFlow.html) 
  of branching and code versioning in git. 
* Code development will be peformed in a forked copy of the repo. Commits will not be made directly to the django-basin3d repo.  Developers will submit a pull request that is then merged by another team member, if another team member is available.
* Each pull request should contain only related modifications to a feature or bug fix.  
* Sensitive information (secret keys, usernames etc) and configuration data (e.g database host port) should not be checked in to the repo.
* A practice of rebasing with the main repo should be used rather that merge commmits.  

## Getting Started

### Prerequisities
django-basin3d is a Django application which requires:

* Django (>=2.0,<2.1)**

** django-basin3d may work on later versions of Django Application Framework, but it has not been tested.

### Get the code

These instructions will get you a copy of the project up and running on your local machine for 
development and testing purposes. 

    $ git clone git@bitbucket.org:BASIN-3D/django-basin3d.git
    $ cd django-basin3d
    

## Develop
Setup virtualenv for development and testing purposes. All django-basin3d tests
are in `example-django`. 

### Example Django Project
There is an example project for testing in directory `example-django`. 
   
Create an Anaconda environment

    conda create -y -n django-basin3d python=3.8
	
Activate the new environment and prepare it for development

	conda activate django-basin3d
	conda develop -npf -n django-basin3d .

Install django-basin3d and its dependencies

	pip install $(cat requirements.txt) pytest-django pytest-cov mypy flake9 pytest-flake8 pytest-mypy type-extensions
	python setup.py develop 
	
	
Migrate the database

	./example-django/manage.py migrate
	
Run the tests

    pytest -v --cov django_basin3d example-django/tests 


Run  the server

    ./example-django/manage.py runserver

    
Create a superuser

    ./example-django/manage.py createsuperuser
    

## Documentation
Sphinx is used to generate documentation. You first need
to create a virtual environment for generating the docs.

    $ source activate django-basin3d
    $ pip install -r docs/requirements.txt
    
Generate the documentation
   
    $ cd docs
    $ make html

Review the generated documentation

    $ open _build/html/index.html

# Install
 
Install a source distribution with pip:

    $ pip install django-basin3d-<version>.tar.gz
    
To get started read the [setup](./docs/setup.rst) documentation

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, 
see the [tags on this repository](https://github.com/BASIN-3D/django-basin3d/tags). 

Workflow for tagging and building release:

1. checkout the version to tag from `master`
1. `git tag -a v[version]-[release] -m "Tagging release v[version]-[release]"`
1. build distribution with `setup.py`
1. `git push origin v[version]-[release]`

## Authors

* **Charuleka Varadharajan** - [LBL](http://eesa.lbl.gov/profiles/charuleka-varadharajan/)
* **Valerie Hendrix**  - [LBL](https://crd.lbl.gov/departments/data-science-and-technology/uss/staff/valerie-hendrix)
* **Danielle Svehla Christianson** - [LBL](https://crd.lbl.gov/departments/data-science-and-technology/uss/staff/danielle-christianson/)


See also the list of [contributors](contributors.txt) who 
participated in this project.

## Copyright

Broker for Assimilation, Synthesis and Integration of eNvironmental Diverse, Distributed Datasets (BASIN-3D) Copyright (c) 2019, The
Regents of the University of California, through Lawrence Berkeley National
Laboratory (subject to receipt of any required approvals from the U.S.
Dept. of Energy).  All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative
works, and perform publicly and display publicly, and to permit other to do
so.

## License

See [LICENSE.md](LICENSE.md) file for licensing details

## Acknowledgments

This research is supported as part of the Watershed Function Scientific Focus Area funded by the U.S. Department of Energy, Office of Science, Office of Biological and Environmental Research under Award no. DE-AC02-05CH11231. This research used resources of the National Energy Research Scientific Computing Center (NERSC), U.S. Department of Energy Office of Science User Facility operated under Contract No. DE-AC02-05CH11231. 
