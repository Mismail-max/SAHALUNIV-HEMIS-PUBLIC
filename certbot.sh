#!/bin/bash


# Define variables
DOMAIN="example.com"
EMAIL="you@example.com"         # Change to your email for cert renewal notifications
WEBROOT_PATH="/var/www/certbot"        # Directory for the HTTP challenge
CERTBOT_DIR="/etc/letsencrypt"         # Certbot directory
CERTBOT_CONF_DIR="$CERTBOT_DIR/live/$DOMAIN"
CERT_FILE="$CERTBOT_CONF_DIR/fullchain.pem"
KEY_FILE="$CERTBOT_CONF_DIR/privkey.pem"

# Install Certbot if not installed
if ! command -v certbot &>/dev/null; then
    echo "Installing Certbot..."
    sudo apt update
    sudo apt install -y certbot
fi

# Create the webroot directory if it doesn't exist
echo "Creating webroot directory at $WEBROOT_PATH..."
sudo mkdir -p $WEBROOT_PATH

# Request the SSL certificate from Let's Encrypt using the webroot plugin
echo "Requesting SSL certificate for $DOMAIN..."
sudo certbot certonly --webroot --webroot-path=$WEBROOT_PATH --email $EMAIL --agree-tos --no-eff-email -d $DOMAIN

# Check if the cert files were generated successfully
if [[ -f "$CERT_FILE" && -f "$KEY_FILE" ]]; then
    echo "✅ Certificate successfully generated:"
    echo " - Key: $KEY_FILE"
    echo " - Cert: $CERT_FILE"
else
    echo "❌ Failed to generate certificate"
    exit 1
fi

# Set up automatic renewal (optional)
echo "Setting up automatic certificate renewal..."
echo "0 0,12 * * * root certbot renew --quiet" | sudo tee -a /etc/crontab > /dev/null

echo "SSL certificate for $DOMAIN is ready!"
