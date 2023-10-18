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
Let's start with update.

```bash
    1  sudo apt update
    2  sudo apt install python3 python3-pip python3-venv
    3  mkdir hello-world
    4  cd hello-world/
    5  python3 -m venv venv
    6  source venv/bin/activate
    7  git clone https://github.com/prabinkc2046/Modular-Web-deployment-with-Apache-Gunicorn-Flask.git
    9  cp Modular-Web-deployment-with-Apache-Gunicorn-Flask/app.py .
   13  pip install Flask
   14  pip install gunicorn
   15  pip freeze
   18  gunicorn -b 0.0.0.0:8000 app:app
   21  deactivate 
```



