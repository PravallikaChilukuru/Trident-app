# Trident App

A Django application with Nginx frontend, using Vagrant for VM setup.

## Architecture

- Jump Host: For SSH access
- Web Server: Django + Nginx + Gunicorn
- DB Server: PostgreSQL, private network

## Setup

1. Install Vagrant and VirtualBox.
2. Create .env file with the following the variable name with the required values
        
        SECRET_KEY #A unique string used to protect Django crytographic operations
        DEGUG=TRUE #It should be false in production for security
        # Database Credentials
        DB_NAME #Set the DB_name for an Database name as per your setup
        DB_USER #Set the DB_user for an Username as per your setup
        DB_PASSWORD #Set the DB_PASSWORD with a password as per your setup
        DB_HOST #Set the DB_Host for an IP as per your setup
        DB_PORT #Default 5432 for postgres sql

        # Infrastructure Static IPs
        IP_WEB_SERVER #Set the IP_WEB_SERVER for an IP as per your setup
        IP_DB_SERVER #Set the IP_DB_SERVER for an IP as per your setup
        IP_JUMP_HOST #Set the IP_JUMP_HOST for an IP as per your setup

3. Install Ruby using RubyInstalller https://rubyinstaller.org/downloads/
4. Navigate to project directory /infra, load the environmental variables by using following commands
    ``` gem install dotenv ```
    ``` ruby -r dotenv -e "Dotenv.load" ```
    - To check if the dot env is loaded properly, use the command
    ``` ruby -r dotenv -e "Dotenv.load; puts ENV['ANY_Varaible-name']" ``` 
5. Run `vagrant up` in infra/ directory.
6. Access the app via jump host.
    ``` vagrant ssh jump -- -A ```


## Snapshot
- There is a cron job which runs everymid night and automatically stores data in DB_Server. To acces this we can connect to the jump host, ssh to web vm and connect to the django server
    ``` psql -h 127.0.0.1 -U <psql User> -d <psql_DB> -c "SELECT id, timestamp, cpu_usage, ram_usage, disk_usage FROM trident_app_systemsnapshot ORDER BY timestamp DESC LIMIT 5;" ```          #Provide the credentials DB_User, DB_Password
    ``` \dt ``` # Lists all the tables
    ``` SELECT * FROM snapshots ```
