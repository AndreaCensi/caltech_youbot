
### Install python2.7 on youbot (Ubuntu 10.04)
The package information on Ubuntu 10.04 is outdated. Python 2.7 and virtualenv 1.7 is missing.
Follow the instructions from:
http://askubuntu.com/questions/101591/how-do-i-install-python-2-7-2-on-10-04

In case the link would die, the instructions are:
1. First install some dependencys:

    sudo apt-get install build-essential
    sudo apt-get install libreadline5-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

2. Then download using the following command:

    cd Downloads/

    wget http://python.org/ftp/python/2.7.2/Python-2.7.2.tgz

3. Extract and go to the dirctory

    tar -xvf Python-2.7.2.tgz && cd Python-2.7.2/

Now install using the command you just tried:

    ./configure
    make
    sudo make altinstall

### Virtual Environments virtualenv
The boot12env packages uses virtualenv 1.7+ which depends on python2.7+. 
The virtualenv packages 1.7+ are also missing in the package list on the youbot (Ubuntu 10.04), as well as python2.7.

1. Start with installing python2.7

2. download the python-virtualenv package. E.g. from: 

    https://launchpad.net/ubuntu/raring/i386/python-virtualenv/1.7.1.2-2 

The package installer will only find the old versions of python, so the python dependencies has to be ignored while installing. 
Install with:

    sudo dpkg -i --ignore-depends=python,python2.7 python-virtualenv_1.7.1.2-2_all.deb
