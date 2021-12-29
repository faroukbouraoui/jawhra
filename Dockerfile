# our base image
FROM odoo:14.0
# copy files required for the app to run
COPY ./custom/addons /mnt/extra-addons
