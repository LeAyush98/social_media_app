#!/bin/bash

# Start MySQL service
service mysql start

# Execute MySQL commands
mysql -e "CREATE DATABASE IF NOT EXISTS assignment;"
mysql -e "CREATE USER 'root'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';"
mysql -e "GRANT ALL PRIVILEGES ON assignment.* TO 'root'@'%';"
mysql -e "FLUSH PRIVILEGES;"
