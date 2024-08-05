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
<html>
  <head>
  </head>
  <body>
    Holberton School
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
HBNB_STATIC_SERVER_FILE_SYS_LINK=/etc/nginx/sites-enabled/default

#1. Create our file
sudo tee $HBNB_STATIC_SERVER_FILE > /dev/null <<EOL
server {
    listen 80 default;
	listen [::]:80 default;

	index index.html index.htm index.nginx-debian.html;

    server_name _;
	error_page 404 = @error_404;
	
	location @error_404 {
		default_type text/html;
		return 404 "Ceci n'est pas une page";
        internal;
	}

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
