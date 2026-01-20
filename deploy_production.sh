#!/bin/bash

# ==============================================================================
# College Management System - Production Deployment Quick Start
# ==============================================================================
# 
# This script automates the production setup process
# Usage: bash deploy_production.sh
#
# ==============================================================================

set -e  # Exit on error

echo "========================================================================"
echo "   College Management System - Production Setup"
echo "========================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==============================================================================
# STEP 1: Check Python
# ==============================================================================

echo -e "${YELLOW}[1/8] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"

# ==============================================================================
# STEP 2: Create Virtual Environment
# ==============================================================================

echo ""
echo -e "${YELLOW}[2/8] Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# ==============================================================================
# STEP 3: Install Dependencies
# ==============================================================================

echo ""
echo -e "${YELLOW}[3/8] Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"

# ==============================================================================
# STEP 4: Generate Secret Key
# ==============================================================================

echo ""
echo -e "${YELLOW}[4/8] Generating SECRET_KEY...${NC}"
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
echo -e "${GREEN}✓ Generated SECRET_KEY${NC}"

# ==============================================================================
# STEP 5: Create .env File
# ==============================================================================

echo ""
echo -e "${YELLOW}[5/8] Creating .env file...${NC}"

if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists. Skipping creation.${NC}"
    echo -e "${YELLOW}   Please verify your settings are correct.${NC}"
else
    cat > .env << EOF
# Generated $(date)
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database - CHANGE THESE VALUES
DB_ENGINE=django.db.backends.postgresql
DB_NAME=college_db
DB_USER=college_user
DB_PASSWORD=change_me_to_secure_password
DB_HOST=localhost
DB_PORT=5432

# Email - Optional
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
EOF
    
    # Restrict file permissions for security
    chmod 600 .env
    
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit .env file and change database credentials!${NC}"
fi

# ==============================================================================
# STEP 6: Create Logs Directory
# ==============================================================================

echo ""
echo -e "${YELLOW}[6/8] Creating logs directory...${NC}"
mkdir -p logs
chmod 755 logs
echo -e "${GREEN}✓ Logs directory created${NC}"

# ==============================================================================
# STEP 7: Collect Static Files
# ==============================================================================

echo ""
echo -e "${YELLOW}[7/8] Collecting static files...${NC}"
export DJANGO_SETTINGS_MODULE=college_project.settings_production
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✓ Static files collected${NC}"

# ==============================================================================
# STEP 8: Run Django Checks
# ==============================================================================

echo ""
echo -e "${YELLOW}[8/8] Running Django security checks...${NC}"
python manage.py check --deploy 2>&1 | grep -E "^(WARNING|ERROR|System check)" || true
echo -e "${GREEN}✓ Django checks completed${NC}"

# ==============================================================================
# COMPLETION MESSAGE
# ==============================================================================

echo ""
echo "========================================================================"
echo -e "${GREEN}✅ Production setup completed!${NC}"
echo "========================================================================"
echo ""
echo "Next Steps:"
echo "1️⃣  Edit .env file with your actual configuration:"
echo "   nano .env"
echo ""
echo "2️⃣  Set up PostgreSQL database:"
echo "   sudo -u postgres psql"
echo "   CREATE DATABASE college_db;"
echo "   CREATE USER college_user WITH PASSWORD 'your_password';"
echo "   ALTER ROLE college_user SET client_encoding TO 'utf8';"
echo "   GRANT ALL PRIVILEGES ON DATABASE college_db TO college_user;"
echo ""
echo "3️⃣  Run migrations on the new database:"
echo "   source venv/bin/activate"
echo "   export DJANGO_SETTINGS_MODULE=college_project.settings_production"
echo "   python manage.py migrate"
echo ""
echo "4️⃣  Create superuser:"
echo "   python manage.py createsuperuser"
echo ""
echo "5️⃣  Test the application:"
echo "   python manage.py runserver --settings=college_project.settings_production"
echo ""
echo "6️⃣  Set up Gunicorn:"
echo "   gunicorn college_project.wsgi:application \\"
echo "     --bind 0.0.0.0:8000 --workers 4"
echo ""
echo "7️⃣  Configure Nginx as reverse proxy"
echo ""
echo "8️⃣  Set up SSL certificate with Certbot"
echo ""
echo "Important Security Reminders:"
echo "  • Keep .env file secure and never commit it"
echo "  • Use strong passwords for database and email"
echo "  • Set up regular backups"
echo "  • Monitor logs: tail -f logs/django.log"
echo "  • Keep Django and dependencies updated"
echo ""
echo "Documentation:"
echo "  See PRODUCTION_DEPLOYMENT.md for detailed instructions"
echo "========================================================================"
echo ""
