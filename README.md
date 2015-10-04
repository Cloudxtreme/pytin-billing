# pytin-billing

Billing system, used internally in justhost.ru. Actually this is the open sourced updated and refactored version.
Development is in progress.

## Requirements

Python 2.7 or higher

Python modules
Django==1.8.3
MySQL-python==1.2.5
django-filter==0.11.0
djangorestframework==3.2.3
idna==2.0
mysql==0.0.1
prettytable==0.7.2
pytils==0.3
pytz==2015.4
requests==2.7.0
wsgiref==0.1.2


## Installation on CentOS 6.x

### Install Python 2.7

yum -y groupinstall "Development tools"

yum -y install zlib-devel
yum -y install bzip2-devel
yum -y install openssl-devel
yum -y install ncurses-devel
yum -y install sqlite-devel
yum -y install libffi-devel libssl-devel

cd /opt
wget --no-check-certificate https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
tar xf Python-2.7.6.tar.xz && cd Python-2.7.6
./configure --prefix=/usr/local
make && make altinstall

ln -s /usr/local/bin/python2.7 /usr/local/bin/python
ln -s /usr/local/bin/pip2.7 /usr/bin/pip

!!! Поправить shebang в yum на этот #!/usr/bin/python2.6 
mcedit /usr/bin/yum

Install PIP: https://pip.pypa.io/en/latest/installing.html
$ wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

Ставим virtualenv
$ pip install virtualenv
$ pip install requests[security]

Далее всё ставим в окружении.
$ useradd pybilling
$ mkdir -p /apps/pybilling
$ chown -R pybilling:pybilling /apps/pybilling
$ cd /apps/pybilling

$ yum -y install mysql mysql-server mysql-devel
$ chkconfig mysqld on
$ /etc/init.d/mysqld start
$ /usr/bin/mysql_secure_installation

edit /etc/my.cnf

    [mysqld]
    collation-server = utf8_unicode_ci
    init-connect='SET NAMES utf8'
    character-set-server = utf8
    
    [client]
    default-character-set=utf8
    
    [mysql]
    default-character-set=utf8


mysql -u root -p
> create database pybilling;
> CREATE USER 'pybilling'@'localhost' IDENTIFIED BY 'password';
> GRANT ALL PRIVILEGES ON pybilling.* TO 'pybilling'@'localhost';
> FLUSH PRIVILEGES;

Чтобы тесты выполнялись
> GRANT CREATE,DELETE ON *.* TO 'pybilling'@'localhost';
> GRANT ALL PRIVILEGES ON test_pybilling.* TO 'pybilling'@'localhost';
> FLUSH PRIVILEGES;

Выполнить 
bash <(curl https://raw.githubusercontent.com/servancho/pytin-billing/master/pybilling/deploy/init.sh)


## REST API

GET, POST, PUT, DELETE
/v1/accounts/[<id>/]

GET, POST, PUT, DELETE
/v1/contacts/[<id>/]

GET, POST, PUT, DELETE
/v1/pdata/[<id>/]

mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u admin -p mysql
mysql -u root -p -e "flush tables;" mysql

[more info coming soon]

./manage.py runserver 127.0.0.1:8018
