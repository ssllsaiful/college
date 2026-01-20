# Production Deployment Checklist

## 1. TURN OFF DEBUG MODE

**File:** `college_project/settings.py`

Change line 28:
```python
# Current (Development):
DEBUG = True

# Change to (Production):
DEBUG = False
```

---

## 2. UPDATE ALLOWED_HOSTS

**File:** `college_project/settings.py`

Change line 30:
```python
# Current (Development):
ALLOWED_HOSTS = []

# Change to (Production):
# Replace with your actual domain/IP address
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '192.168.x.x']
# Or for all subdomains:
ALLOWED_HOSTS = ['*.yourdomain.com', 'yourdomain.com']
```

---

## 3. SECURE SECRET KEY

**File:** `college_project/settings.py`

⚠️ **CRITICAL:** The current SECRET_KEY is exposed! Generate a new one:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Replace line 25:
```python
# Current (EXPOSED - CHANGE THIS):
SECRET_KEY = 'django-insecure-28!l8xu#7$3exgz^)g4g=yr&8npl=)i5c3i++-num7o++b141b'

# Change to (new generated key):
SECRET_KEY = 'your-new-secure-key-here'
```

Or use environment variables (recommended):
```python
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key')
```

---

## 4. DATABASE CONFIGURATION

⚠️ **SQLite NOT recommended for production!**

For production, use PostgreSQL:

```python
# Current (Development):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Change to (Production):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'college_db',
        'USER': 'college_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Or using environment variables:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

---

## 5. SECURITY SETTINGS (Add to settings.py)

Add these security headers:

```python
# Security Settings for Production
SECURE_SSL_REDIRECT = True              # Redirect HTTP to HTTPS
SESSION_COOKIE_SECURE = True            # Only send session cookie over HTTPS
CSRF_COOKIE_SECURE = True               # Only send CSRF cookie over HTTPS
SECURE_BROWSER_XSS_FILTER = True        # XSS protection
SECURE_CONTENT_SECURITY_POLICY_REPORT_ONLY = True
X_FRAME_OPTIONS = 'DENY'                # Prevent clickjacking
SECURE_HSTS_SECONDS = 31536000          # HTTP Strict Transport Security (1 year)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## 6. STATIC FILES CONFIGURATION

For production, collect static files:

```bash
# Collect all static files to STATIC_ROOT
python manage.py collectstatic --noinput
```

The files will be collected to: `staticfiles/`

---

## 7. CREATE ENVIRONMENT FILE

Create `.env` file in project root:

```
# Security
SECRET_KEY=your-secure-key-here
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=college_db
DB_USER=college_user
DB_PASSWORD=secure_password_here
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (for media files - optional)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

---

## 8. UPDATE settings.py TO USE ENVIRONMENT VARIABLES

Add to the top of `settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Security
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}
```

Install python-dotenv:
```bash
pip install python-dotenv
```

---

## 9. PRODUCTION CHECKLIST

Before deploying, verify:

```bash
# Run Django security checks
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput

# Run migrations on production database
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser
```

---

## 10. WEB SERVER SETUP

### Option A: Using Gunicorn + Nginx

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Run with Gunicorn:**
```bash
gunicorn college_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

**Create Nginx config** (`/etc/nginx/sites-available/college`):
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /path/to/college/staticfiles/;
    }

    location /media/ {
        alias /path/to/college/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Option B: Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DEBUG=False
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "college_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: college_db
      POSTGRES_USER: college_user
      POSTGRES_PASSWORD: secure_password

  web:
    build: .
    command: gunicorn college_project.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=False
      - DB_NAME=college_db
      - DB_USER=college_user
      - DB_PASSWORD=secure_password
      - DB_HOST=db
```

---

## 11. SSL/HTTPS SETUP

### Using Let's Encrypt with Certbot:

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate SSL certificate
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Update Nginx config to use SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renew certificates
sudo certbot renew --dry-run
```

---

## 12. MONITORING & LOGGING

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

Create logs directory:
```bash
mkdir -p logs
```

---

## SUMMARY OF CHANGES NEEDED

| Setting | Development | Production |
|---------|------------|-----------|
| DEBUG | True | **False** ❌ |
| SECRET_KEY | Exposed | New secure key ❌ |
| ALLOWED_HOSTS | [] | Your domain ❌ |
| DATABASES | SQLite | PostgreSQL ❌ |
| SSL/HTTPS | No | Yes ❌ |
| SECURE_SSL_REDIRECT | False | True ❌ |
| SESSION_COOKIE_SECURE | False | True ❌ |
| Static Files | Served by Django | Served by Nginx ❌ |

---

## QUICK PRODUCTION SETUP SCRIPT

```bash
#!/bin/bash

echo "🔧 Production Setup Starting..."

# Generate new secret key
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
echo "Generated SECRET_KEY: $SECRET_KEY"

# Create .env file
cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=college_db
DB_USER=college_user
DB_PASSWORD=change_me
DB_HOST=localhost
DB_PORT=5432
EOF

echo "✓ Created .env file"

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary python-dotenv

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Run security checks
python manage.py check --deploy

echo "✅ Production setup complete!"
echo "⚠️  Don't forget to:"
echo "   1. Set DATABASE credentials in .env"
echo "   2. Update ALLOWED_HOSTS in .env"
echo "   3. Change SECRET_KEY to the generated one"
echo "   4. Run: python manage.py createsuperuser"
echo "   5. Configure Nginx/Gunicorn"
echo "   6. Set up SSL certificate"
```

Save as `production_setup.sh` and run:
```bash
chmod +x production_setup.sh
./production_setup.sh
```

---

## DEPLOYMENT PLATFORMS

### Popular Options:
1. **Heroku** - Simple, automatic scaling
2. **PythonAnywhere** - Python-specific hosting
3. **Digital Ocean** - Affordable VPS
4. **AWS** - Scalable, complex
5. **Google Cloud** - Enterprise-grade
6. **Railway.app** - Modern, easy deployment

---

## NEED HELP?

For production deployment support:
- Check Django deployment checklist: https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
- Review your hosting provider's documentation
- Test thoroughly in staging environment first
