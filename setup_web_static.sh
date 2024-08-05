#!/usr/bin/env bash
# 0-setup_web_static.sh
# Written by Ignatius K <ignatiuskisekka@gmail.com>
#
# Script that sets up web server for
# static file deployment


# Install nginx if not installed
if ! command -v nginx &> /dev/null
then
	echo "Installing Nginx ..."
	sudo apt-get update
	sudo apt-get install -y nginx
	echo "Nginx installed successully"
fi

# Create the required folder if it doesn't exist
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# Create a Test HTML file
TEST_HTML_FILE=/data/web_static/releases/test/index.html
cat <<EOL > $TEST_HTML_FILE
<!DOCTYPE html>
<html>
<head>
	<title>Wow</title>
</head>
<body style="background-color: #f0f0f0; text-align: center; font-family: Arial, sans-serif;">
	<h1 style="color: #333; font-size: 2em;">Welcome to Alexa!</h1>
	<p style="color: #555; font-size: 1.2em;">Just know <strong>Ignatius</strong>.</p>
</body>
</html>
EOL

# Link our test folder to Nginx's current
TARGET=/data/web_static/releases/test/
SYMLINK=/data/web_static/current
if [ -L "$SYMLINK" ]
then
	sudo rm "$SYMLINK"
fi
sudo ln -s "$TARGET" "$SYMLINK"
echo "Created link $SYMLINK -> $TARGET"

# Give ownership to user and group `ubuntu`
sudo chown -R ubuntu:ubuntu /data/


# Add configuration to Nginx
ALIAS_PATH=/hbnb_static
HBNB_STATIC_SERVER_FILE=/etc/nginx/sites-available/hbnb_static
HBNB_STATIC_SERVER_FILE_SYS_LINK=/etc/nginx/sites-enabled/hbnb_static

#1. Create our file
sudo tee $HBNB_STATIC_SERVER_FILE > /dev/null <<EOL
server {
    listen 80;
	listen [::]:80;

	index index.html index.htm index.nginx-debian.html;

    server_name myalexa.tech;

    location $ALIAS_PATH {
        alias $SYMLINK/;
    }

    # Other configurations
}
EOL

#2. Create link in enabled sites
if [ -L $HBNB_STATIC_SERVER_FILE_SYS_LINK ]
then
	sudo rm $HBNB_STATIC_SERVER_FILE_SYS_LINK
fi
sudo ln -s $HBNB_STATIC_SERVER_FILE $HBNB_STATIC_SERVER_FILE_SYS_LINK

#3. Test new site configuration
sudo nginx -t
if [ $? -eq 0 ]
then
	echo -e "Configuration test passed\nRestarting Nginx ........."
	sudo systemctl restart nginx
else
	echo "Nginx configuration test failed"
fi
