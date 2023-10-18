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

## Setting up process manager using systemd

```bash
     sudo touch  /etc/systemd/system/flask-server.service
     sudo cp flask-server.service /etc/systemd/system/flask-server.service 
     sudo systemctl daemon-reload 
     sudo systemctl start flask-server.service 
     sudo systemctl status flask-server.service 
     sudo systemctl enable flask-server.service 

```





