# Modular Web Deployment: Apache, Gunicorn, and Flask (with implementation demo in AWS)

In a traditional LAMP stack deployment of web application, apache server handlesthe incoming request and communicates with PHP interpreter embedded within the processess of apache to process the dynamic content. Apache server is tighly coupled with PHP. for example, LAMP stack deploying of PHP application with mod_php.
In a separation approach, in contrast to traditional method, the apache server handles the incoming request and forward it to the dedicated server or process to process the dynamic content. In traditional approach, the entire process happens in the same environment while the components are separated and independent in separation approach for example web server with mod_wsgi with python application. Having separation of component leverages the scalability allowing to add instances to run application. This will handle more request concurrently and with less stress on the resources. Also allows the better resource optimization of the dedicated server with the specific need of application.

So separation approach is preferred for its scalability, flexibility and better resource optimization.

In this demo,
I will be using decoupling method to deploy Flask application. Instead of embedding Python interpreter within the processes of Apache, they will run separately and independently in a dedicated server. I will walk you through following:

1. Set up Flask application server as a backend 
2. Set up Apache web server as a frontend

I am going to implement this in Linode first and later in  AWS.

Let's get started :)

# Configuring the Flask Application Server
## Deploying Flask Application in a Virtualized Environment
Run the following command step by step to deploy our flask application using gunicorn. Finally, our application can be accessible at http://server-IP:8000 

```bash
     sudo apt update
     sudo apt install python3 python3-pip python3-venv
     mkdir hello-world
     cd hello-world/
     python3 -m venv venv
     source venv/bin/activate
     git clone https://github.com/prabinkc2046/Modular-Web-deployment-with-Apache-Gunicorn-Flask.git
     cp Modular-Web-deployment-with-Apache-Gunicorn-Flask/app.py .
     pip install Flask
     pip install gunicorn
     pip freeze
     gunicorn -b 0.0.0.0:8000 app:app
```
After this, our flask application is accessible at http://server_ip/domain:8000. If the appliation is running behind a firewall, allow communication on port 8000 for incoming traffic.

However, this is not suitable for production environment. I will show how to use systemd and also supervisior to manage and monitor our flask application. The process manager like systemd and tools like supervisor provides features such as supervision, logging and monitoring.

## Setting up process manager with systemd

```bash     
     deactivate
     sudo touch  /etc/systemd/system/flask-server.service
     sudo cp ../config/flask-server.service /etc/systemd/system/flask-server.service 
     sudo systemctl daemon-reload 
     sudo systemctl start flask-server.service 
     sudo systemctl status flask-server.service 
     sudo systemctl enable flask-server.service 
```

At this stage, virtual environment is deactivated and the flask application is running in the background under the supervision of systemd. We can access our server at http://server_ip/domain:8000. In the next, I will show how to use supervisior to manage and monitor flask application.

## Enabling Process Supervision through systemd

```bash
	sudo systemctl stop flask-server.service
	sudo apt install supervisor
	sudo touch /etc/supervisor/conf.d/flask-server.conf
	sudo cp ../config/flask-server.conf /etc/supervisor/conf.d/flask-server.conf
	sudo supervisorctl reread
	sudo supervisorctl update
	sudo supervisorctl status flask-server
```
There you go! we've just use supervisor to manage our flask application. I am happy with systemd so I will keep using systemd in this demo.

So we are done with the setting up backend flask application server. Let's go ahead and tackle with configuring apache to server as frontend server.

# Configuring Apache as a Frontend Proxy Server
In this setup, I will spin up a new linux server and walk you through the step to configure Apache to act as reverse proxy. Let's get started:

```bash
	sudo apt update
	sudo apt install apache2 -y
	sudo touch /etc/apache2/sites-available/flaskapp.conf
	sudo cp ../config/flaskapp.conf /etc/apache2/sites-available/flaskapp.conf
	sudo a2enmod proxy
	sudo a2enmod proxy_http
	cd /etc/apache2/sites-available/flaskapp.conf
	sudo a2ensite flaskapp.conf
	sudo systemctl restart apache2.service
```

Let's look at few line used in flaskapp.conf:
```
<VirtualHost *:80>
    ServerName hello-world.prabinkc.com
    ProxyPass / http://172.105.174.176:8000/
    ProxyPassReverse / http://172.105.174.176:8000/

    ErrorLog ${APACHE_LOG_DIR}/flaskapp.error.log
    CustomLog ${APACHE_LOG_DIR}/flaskapp.access.log combined
</VirtualHost>
```
This is my config. What ProxyPass directive does is that any request to our apache server at root url for example: http://hello-world.prabinkc.com will be forwarded to the backend flask server at http://172.105.174.176:8000/. And what ProxyPassReverse does is that it ensures that the response that came back from the backend server to appear as if it came from the proxy server itself. Essentially, adjusting the header in the response from the backend server to match with the proxy's header. 

## Accessing the flask application via proxy server
Point your url to the front end proxy server. in my case, http://flaskapp.prabinkc.com and you will see the message from the backend server.

## Access the log 
```bash
sudo tail -f /var/log/apache2/flaskapp.access.log
``` 

# Enabling SSL Encryption with Let's Encrypt
Install following packages:
```bash
sudo apt install certbot python3-certbot-apache
```
Then
```bash
sudo certbot --apache
```

Answer as follow:
```bash
apache-server@localhost:~$ sudo certbot --apache
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Enter email address (used for urgent renewal and security notices)
 (Enter 'c' to cancel): prabin.devops.demo@gmail.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.3-September-21-2022.pdf. You must
agree in order to register with the ACME server. Do you agree?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing, once your first certificate is successfully issued, to
share your email address with the Electronic Frontier Foundation, a founding
partner of the Let's Encrypt project and the non-profit organization that
develops Certbot? We'd like to send you email about our work encrypting the web,
EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: N
Account registered.

Which names would you like to activate HTTPS for?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: hello-world.prabinkc.com
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): 1
Requesting a certificate for hello-world.prabinkc.com

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/hello-world.prabinkc.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/hello-world.prabinkc.com/privkey.pem
This certificate expires on 2024-01-16.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for hello-world.prabinkc.com to /etc/apache2/sites-available/flaskapp-le-ssl.conf
Congratulations! You have successfully enabled HTTPS on https://hello-world.prabinkc.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

# Access via a Secure Connection

Try accessing the front end server, in my case, https://hello-world.prabinkc.com
and there you have it!

# Deploying on AWS Cloud
I've completed the above implementation steps on Linode, and now we're transitioning to AWS for our project. I'll be providing video demos for each phase of the implementation in AWS.

# Hello-world-project Architecture
Here's a visual representation of our architecture within the AWS VPC. The Flask application server is placed in the private subnet to keep it hidden from the internet. However, we'll utilize a NAT Gateway for system updates and software installations. Apache will reside in the public subnet as it needs to be accessible by the public.


```

         _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ Hello-world-project-vpc_ _ _ _ _ _ _ _ _ _ _
        |                                                                               |
        |       _________________________Availability Zone___________________           |
        |       |                                                            |          |
        |       |                                                            |          |
        |       |       ____Public-SN___                ___Private-SN___     |          |
        |       |       |               |               |               |    |          |
        |       |       |               |               |               |    |          |
        |       |       |               |               |               |    |          |
        |       |       |       🛠️       |               |       🌐      |    |          |
        |       |       |   ApacheServer|               | Flask App     |    |          |
        |       |       |               |               |   Server      |    |          |       
        |       |       |__ ____________|               |_______________|    |          |
        |       |____________________________________________________________|          |       
        |_______________________________________________________________________________|
 

```

# Planning
In the world of AWS, meticulous planning is essential for successful resource deployment. Here's the plan we'll follow:

1. Create a VPC (Virtual Private Cloud):

Establish a VPC named "hello-world-project-vpc" in the Asia Pacific region with a CIDR block of 10.0.0.0/16.

[VPC creation demo](https://youtu.be/TM8UIQqkGdM)

# Create Subnets:

## Set up two subnets:
1. Private-SN with a CIDR block of 10.0.1.0/24.
2. Public-SN with a CIDR block of 10.0.2.0/24.

The private subnet will remain hidden from the outside world, while the public subnet will be accessible from the internet.

[Subnet creation](https://youtu.be/coy5KgrHP-o)

# Create Routing Tables:

Develop two routing tables, each corresponding to the Public and Private Subnets.
1. Private-RT:
 Enables routing within the VPC CIDR block and is equipped with a NAT Gateway to allow instances in the private subnet to access the internet for updates and software installations. This routing table is associated with the private subnet.

2. Public-RT: Provides internet access via an Internet Gateway and is associated with the public subnet.

[Routing setup](https://youtu.be/XW7OxxSbALE)

# Create Security Groups:

We'll configure two security groups:

1. Apache-SG: Permits HTTP, HTTPS, and SSH traffic.
2. Flask-SG: Allows any traffic originating from members of the Apache-SG.

[Security group setup](https://youtu.be/EtkBqhfg07E)

# Launch Instances:

Launch Ubuntu instances in both the public and private subnets:

1. Backend-Flaskserver with no public IP.
2. Frontend-ApacheServer with a public IP.

[Launching instances](https://youtu.be/gflU9gosKkk)

# Access Private Instances via a Jump Host:

Set up the ability to access private instances through a jump host. Here's how:

	Add the private key to the SSH agent: ssh-add /path/to/private/key.
	Confirm that the private key is added by listing: ssh-add -l.
	Forward the private key to the remote server using agent forwarding: ssh -A ubuntu@publicIP.
	Access the private subnet with the private IP: ssh ubuntu@privateIP.

[Accessing private instances](https://youtu.be/e-tIy1Or5tM)

# Configure the Private EC2 Instance:

Ensure the private instance is fully configured:

1. Update the system
2. Set up the hostname: Backend-flask-server and update /etc/hosts file
3. Install Python3, Python3-pip, Python3-venv.
4. Clone the code repository
4. Set up a virtualized environment and run Flask using Gunicorn.
5. Set up a  process manager using systemd to monitor and manage our flask application

[Deploying a Flask App with Gunicorn on an EC2 Instance in the Private Subnet.](https://youtu.be/DrIxRCfCzU4)

# Configure the Frontend Apache Server as a Reverse Proxy:

Configure the frontend Apache server for the reverse proxy:
1. Update sytem
2. Set up the hostname: Frontend-apache-server and update /etc/hosts/ file
3. Install and configure Apache for reverse proxy.
[Configuring Apache as a Reverse Proxy on the Instance in the Public Subnet.](https://youtu.be/cFkdBvNqkuI)

