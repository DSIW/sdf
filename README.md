# SDF Project ![travis-ci](https://travis-ci.org/DSIW/sdf.svg)

## Getting started

1. Clone this repo via `git clone https://github.com/DSIW/sdf.git`
1. Install python3 via package manager (e.g. `pacman -S python`)
1. Install `virtualenv` and `virtualenvwrapper` via package manager (e.g. `pacman -S python-virtualenv python-virtualenvwrapper`)
1. Add virtualenvwrapper to your zsh plugins if your're using oh-my-zsh and restart your terminal
1. `cd sdf`
1. Create a new environment named `django_sdf` via `mkvirtualenv django_sdf`
1. Install required packages via `pip install -r requirements.txt`
1. Reset your DB via `./reset_db.sh`. This will migrate your DB and some seed data will be imported.
1. Open the app via `http://localhost:3001`

## Setup nginx (optional)

1. Install nginx via package manage (e.g. `pacman -S nginx`)
1. `cp config/django_sdf.conf /etc/nginx/conf.d`
1. Start and enable nginx service (e.g. `systemctl start nginx.service; systemctl enable nginx.service`)
1. Now you can request the site via `http://sdf.localhost` if local server is running via `python manage.py runserver 3001`.

## Requirements

* `decorator`: Required by `ipython`
* `django-braces`: Mixins for views. E.g. FormMessagesMixin for Django's generic views
* `django-extensions`: Enhanced commands: `./manage.py (show_urls|validate_templates|shell_plus|runserver_plus)`
* `invoke`: Invoke commands
* `ipython`: Interactive shell with history support. Run `./manage.py shell_plus`
* `ipython-genutils`: Required by `ipython`
* `path.py`: Required by `ipython`
* `pexpect`: Required by `ipython`
* `pickleshare`: Required by `ipython`
* `ptyprocess`: Required by `ipython`
* `python-dateutil`: Required by `./reset_db.sh`
* `simplegeneric`: Required by `ipython`
* `six`: Required by `django-extensions`
* `traitlets`: Required by `ipython`
* `Werkzeug`: Optional dependency of `django-extensions`
* `wheel`: required for installation of pure python and native C extension packages
* `django-watson`: Required for searching

## Notices

* We use [Material Design](http://materializecss.com)
* We use [Material Icons](https://www.google.com/design/icons/)
* We use [Fontawesome Icons](http://fontawesome.io/icons) if no icon in Material Design exists

## Getting search to work

For `watson` to work, you need to execute the following tasks:

1. `manage.py syncdb`
1. `manage.py installwatson`

If you already have a populated database, you also need to build the indices:

1. `manage.py buildwatson`


## Getting Pillow to work

Pillow is needed for image processing.
For `Pillow` to work, you need to execute the following tasks:

1. install `python-image` via package manager (e.g. `apt-get install python-image`
1. `pip3 install -r requirements.txt`

## Important Style Guide

### Python

* 4 Spaces instead of Tabs for indentation

### Git

I recommend using git in terminal, so you have full control. You only need a couple of commands (`pull,commit,status,push,checkout,add`).

1. `cp config/gitconfig ~/.gitconfig`
1. Change your name and email in `~/.gitconfig`

* Branch `master` contains code which works and will be deployed.
* Branch `develop` is our development branch. Every feature branch will be merged into the `develop`.
* Use your own feature branches for every ticket named like `feature-31/username-topic`. This branch is for one person and its history can be changed (e.g. after rebasing).
* Write commit messages like `Verb topic`. Verb could be one of Add, Fix, Refactor, Remove,...
  Example: `Add user authentication`
* Rebase/Squash your history if needed before merging in `develop`, so there is only one commit to merge.
* **Important**: Use `git checkout develop; git pull --rebase` for updating the current `develop` branch from remote, so no useless commit messages like `Merge branch 'master' of git://...` will be created. (see http://gitready.com/advanced/2009/02/11/pull-with-rebase.html)
* Update changes of `develop` to your current feature branch via `git checkout feature-31/user-topic; git rebase develop`
