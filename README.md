# 📝 BlogSpot Backend

**BlogSpot Backend** is a **RESTful API** built using **Django** and **Django REST Framework**, serving as the backend for a blogging platform. It supports **JWT-based authentication**, **blog post management**, and **media uploads via Cloudinary**. The system is **securely deployed** on **AWS EC2** with **Gunicorn**, **Nginx**, and **Let's Encrypt SSL** for HTTPS support.

---

##  Features

- 🔐 **User Authentication**: Register, login, and manage users via JWT tokens.  
- 📰 **Post Management**: Create, read, update, and delete blog posts.  
- ☁️ **Media Storage**: Integrates with **Cloudinary** for image and media uploads.  
- 🔒 **CORS Support**: Enables secure cross-origin requests from the frontend.  
- 🛠️ **Admin Panel**: Django admin interface for managing users and posts.  
- 🌐 **HTTPS**: Secured using **Let's Encrypt SSL Certificate**.

---

## 🛠 Tech Stack

| Category      | Technology                        |
|---------------|-----------------------------------|
| Framework     | Django, Django REST Framework     |
| Database      | PostgreSQL                        |
| Server        | Gunicorn, Nginx                   |
| Deployment    | AWS EC2 (Ubuntu 20.04+)           |
| Media Storage | Cloudinary                        |
| SSL           | Let’s Encrypt                     |

---

## 📋 Prerequisites

- Python 3.8+  
- `pip` and `virtualenv`  
- AWS EC2 instance (Ubuntu 20.04+)  
- Cloudinary account  
- Domain name (optional but recommended for HTTPS)  
- Git

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/nikhilrajpk/blogSpot_backend.git
cd blogSpot_backend
2. Create and Activate Virtual Environment

python3 -m venv env
source env/bin/activate
3. Install Dependencies

pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file:


touch .env
Add the following:

env

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
5. Update Django Settings
Edit blogspot/settings.py:

python

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-ec2-public-ip', 'your-domain']
CSRF_TRUSTED_ORIGINS = ['https://your-domain']
CORS_ALLOWED_ORIGINS = ['https://your-frontend-domain']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
6. Run Migrations

python manage.py migrate
7. Collect Static Files

python manage.py collectstatic
8. Run Locally

python manage.py runserver
Access the admin panel:
http://localhost:8000/admin/

To create an admin user:

python manage.py createsuperuser
☁️ Deployment on AWS EC2
Set Up EC2 Instance
Launch EC2 with Ubuntu 20.04

Open ports: 22, 80, and 443

Install Dependencies

sudo apt update
sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx
Configure Gunicorn
Create file:


sudo nano /etc/systemd/system/gunicorn_service.service
Paste:

ini

[Unit]
Description=gunicorn daemon for Blogspot
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/blogspot/blogSpot_backend
Environment="PATH=/home/ubuntu/blogspot/blogSpot_backend/env/bin"
ExecStart=/home/ubuntu/blogspot/blogSpot_backend/env/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 blogspot.wsgi:application

[Install]
WantedBy=multi-user.target
Enable and start:


sudo systemctl enable gunicorn_service
sudo systemctl start gunicorn_service
Configure Nginx
Create config:

sudo nano /etc/nginx/sites-available/blogspot
Paste the following:

nginx

server {
    listen 80;
    server_name your-ec2-public-ip your-domain;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your-ec2-public-ip your-domain;

    ssl_certificate /etc/letsencrypt/live/your-domain/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ubuntu/blogspot/blogSpot_backend/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/blogspot/blogSpot_backend/media/;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
Enable and restart Nginx:


sudo ln -s /etc/nginx/sites-available/blogspot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
Set Up SSL

sudo certbot --nginx -d your-domain
Set File Permissions

sudo chown -R www-data:www-data /home/ubuntu/blogspot/blogSpot_backend/staticfiles
sudo chmod -R 755 /home/ubuntu/blogspot/blogSpot_backend/staticfiles
🌐 Access URLs
Admin Panel: https://your-domain/admin/

API Root: https://your-domain/api/

🤝 Contributing
Fork the repository

Create your branch:


git checkout -b feature-name
Make changes and commit:

git commit -m "Add feature"
Push your branch:

git push origin feature-name
Open a Pull Request 🎉
