# Installation
This is mostly just a dump of my process as I was transferring the code to the server.
Hence, it is oriented around Ubuntu/Debian, though there's no in theory it'll work
on most Unixes - I developed this workig from Arch!
<br/>
## Users

These guys should have no permanent storage space
This is mostly enforced by deploy.sh, but make sure they don't have home dirs!
```bash
sudo useradd mallory
sudo useradd malloryt
```

Limit the number of processes these guys can open
We wouldn't want someone taking down the server, would we now?
Edit: `/etc/security/limits.conf`
Add: 
```
mallory hard nproc 100
malloryt hard nproc 100
```
(Or to taste)
<br/>
## Stuff that's probably installed anyway
+ python2
+ python2-{subprocess, timeit}
+ timeout
+ time
+ git
<br/>
## Lamp
### Ubuntu
```bash
sudo apt-get install lamp-server^
```

### Debian
```bash
sudo apt-get install apache2
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo apt-get install php5 php-pear
```
<br/>
## SQL setup
```
mysql -u root -p
> CREATE DATABASE linkgame;
> GRANT ALL PRIVILEGES ON linkgame.* TO '$user'@'localhost' IDENTIFIED BY '$password'
> USE linkgame;
> CREATE TABLE tests ( ID BIGINT PRIMARY KEY AUTO_INCREMENT, uid VARCHAR(100) UNIQUE NOT NULL, testStatus TINYINT SIGNED NOT NULL, debug TEXT );
> CREATE TABLE tournament ( ID BIGINT PRIMARY KEY AUTO_INCREMENT, uid VARCHAR(100) NOT NULL, placementID INT NOT NULL, timeTaken INT NOT NULL, debug TEXT );
```
<br/>
## Java 8
required to run the JARs

### Ubuntu
```bash
sudo apt-get install openjdk-8-jdk
```

### Debian
Edit: `/etc/apt/sources.list.d/java-8-debian.list`
Add:
```sources.list
deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main
deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main

Run:
```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886
sudo apt-get update
sudo apt-get install oracle-java8-installer
sudo apt-get install oracle-java8-set-default
```
Verify that we're running Java 8:
```bash
java -version
```
<br/>
## Groovy
sudo apt-get install groovy
<br/>
## PHP settings
```bash
sudo apt-get install php5-ldap
sudo a2enmod ldap
sudo apt-get install php5-mysqlnd
```
Edit: `/etc/php5/apache2/php.ini`
Add: `extension=mysqli.so`
Modify: `memory_limit`, `upload_max_filesize`, `post_max_size`
to something reasonable. Generally, the latter two should be less
than the former. 
<br/>
## Python
```bash
sudo apt-get install python-pip python3
sudo pip install mysql mysql-connector
```
<br/>
## Code setup
```bash
git clone https://github.com/Pavlos1/linkgame_tournament_server
cd linkgame_tournament_server
```
write appropriate starting placements to `sol.txt`
```bash
cp db.example.php db.php
```
Edit: `db.php` and add credentials
```bash
cp db.example.py db.py
```
Edit: `db.py` with the same credentials
<br/>
## HTTPS
I'm using Let's Encrypt.
```
if externally accessible {
	See: https://certbot.eff.org/#debianjessie-apache
	See: https://backports.debian.org/Instructions/#index2h2
} otherwise {
	See: http://serverfault.com/questions/750902/how-to-use-lets-encrypt-dns-challenge-validation
}

See: [https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html]
```
<br/>
## Spinup
```bash
./deploy.sh
./rundaemons.sh
```
<br/>
## Update
```bash
git pull origin master
GOTO: Spinup
```
