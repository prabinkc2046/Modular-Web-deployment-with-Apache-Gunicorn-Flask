# Modular Web Deployment with Apache + Gunicorn + FLask

In a traditional LAMP stack deployment of web application, apache server handlesthe incoming request and communicates with PHP interpreter embedded within the processess of apache to process the dynamic content. Apache server is tighly coupled with PHP. for example, LAMP stack deploying of PHP application with mod_php.
In a separation approach, in contrast to traditional method, the apache server handles the incoming request and forward it to the dedicated server or process to process the dynamic content. In traditional approach, the entire process happens in the same environment while the components are separated and independent in separation approach for example web server with mod_wsgi with python application. Having separation of component leverages the scalability allowing to add instances to run application. This will handle more request concurrently and with less stress on the resources. Also allows the better resource optimization of the dedicated server with the specific need of application.

So separation approach is preferred for its scalability, flexibility and better resource optimization.

In this demo,
I will be using decoupling method to deploy Flask application. Instead of embedding Python interpreter within the processes of Apache, they will run separately and independently in a dedicated server. I will walk you through following:
1. Set up Flask application server as a backend 
2. Set up Apache web server as a frontend

Let's get started :)

# Setting up Flask application server
## Deploying Flask applicatin in virtualised environment
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

## Setting up process manager with supervisor

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

# Installing and Configuring Apache as frontend proxy web server
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

# Secure connection with let's encrypt
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

# Access over encrypted connection

Try accessing the front end server, in my case, https://hello-world.prabinkc.com
and there you have it!

We have configured apache to serve as a frontend web server while the backend server is dedicated to handle the dynamic content. In this appraoch, frontend can focus on things like ssl termination, serving static page without having to involve flask as well as load balancing. In other demo, I will walk you through configuring and setting up apache as a load balancing server. See you then.

# AWS Implementation
I've done everything so far in the Linode. In the next, I will implement our project in AWS.

# Planning
Planning is key when it comes to deploying resources in aws.

1. create vpc
2. create public and private subnet in the same availablity zone
3. Create route table for private and public subnet
4. Create Security group for flask app server (backend)  and frontend apache server 
5. Set up Nat Gateway for instances in private subnet to access internet
6. Set up instance in public subnet as bastion host to access instance in private subnet
7. Configure Flask application server as backend server
8. Configure Apache in instance as frontend web server
9. Set up ssl with let's encrypt for secure connection
10. Test

# Application Deployment  Architecture

# VPC Architecture

# VPC Architecture

```bash
	..............................................Hello-world-project-VPC...........
	|										|
	|	......................................Availability Zone.......		|
	|	|							     |		|
	|	|							     |		|
	|	|	......Public-SN..		..Private-SN....     |		|	    	    		
	|	|	|		|		|		|    |		|
	|	|	|		|		|		|    |		|
	|	|	|		|		|		|    |		|
	|	|	|	🛠️	|		|	🌐      |    |		|
	|	|	|   ApacheServer|		| Flask App 	|	        |  
	|	|	|		|		|   Server	|    |		|	
	|	|	.................		................     |		|		 
	|	|............................................................|		|
	|										|
	................................................................................
```


