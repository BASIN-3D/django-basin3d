## How to contribute to django-basin3d

## Quick Links
Coming soon

## Development Practices
* django-basin3d uses the [GitFlow model](https://datasift.github.io/gitflow/IntroducingGitFlow.html) 
  of branching and code versioning in git. 
* Code development will be peformed in a forked copy of the repo. Commits will not be made directly to the django-basin3d repo.  Developers will submit a pull request that is then merged by another team member, if another team member is available.
* Each pull request should contain only related modifications to a feature or bug fix.  
* Sensitive information (secret keys, usernames etc) and configuration data (e.g database host port) should not be checked in to the repo.
* A practice of rebasing with the main repo should be used rather that merge commmits.  

## Get the code

These instructions will get you a copy of the project up and running on your local machine for 
development and testing purposes. 

    $ git clone git@bitbucket.org:BASIN-3D/django-basin3d.git
    $ cd django-basin3d

## Develop
Setup virtualenv for development and testing purposes. All django-basin3d tests
are in `example-django`. 

See Example Django Project section on [README.md](README.md) for example project.

## Documentation
Sphinx is used to generate documentation. 

You first need to create a virtual environment for generating the docs and install docs requirements.

    $ pip install -e ".[docs]"
    
Generate the documentation
   
    $ cd docs
    $ make html

Review the generated documentation

    $ open _build/html/index.html

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, 
see the [tags on this repository](https://github.com/BASIN-3D/django-basin3d/tags). 

Workflow for tagging and building release:

1. checkout the version to tag from `master`
1. `git tag -a v[version]-[release] -m "Tagging release v[version]-[release]"`
1. build distribution with `setup.py`
1. `git push origin v[version]-[release]`


