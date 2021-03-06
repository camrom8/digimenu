#!/bin/bash
set -e

# read docker secrets into env variables
export DJANGO_SUPERUSER_PASSWORD=$(cat /run/secrets/django_superuser_password)
export DJANGO_SUPERUSER_MAIL=$(cat /run/secrets/django_superuser_mail)
export DB_PASSWORD=$(cat /run/secrets/db_password)
export SECRET_KEY=$(cat /run/secrets/secret_key)
export EMAIL_HOST_USER=$(cat /run/secrets/email_host_user)
export EMAIL_HOST_PASSWORD=$(cat /run/secrets/email_host_password)
export AWS_ACCESS_KEY_ID=$(cat /run/secrets/aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(cat /run/secrets/aws_secret_access_key)
export AWS_STORAGE_BUCKET_NAME=$(cat /run/secrets/aws_storage_bucket_name)


# run db migrations (retry on error)
while ! python3 /opt/digimenu/manage.py migrate 2>&1; do
  sleep 5
done

# Create Superuser if required
if [ "$DJANGO_SKIP_SUPERUSER" == "true" ]; then
  echo "↩️ Skip creating the superuser"
else
  if [ -z ${DJANGO_SUPERUSER_NAME+x} ]; then
    DJANGO_SUPERUSER_NAME='admin'
  fi
  if [ -z ${DJANGO_SUPERUSER_MAIL+x} ]; then
    DJANGO_SUPERUSER_MAIL='admin@example.com'
  fi
  if [ -z ${DJANGO_SUPERUSER_PASSWORD+x} ]; then
    if [ -f "/run/secrets/django_superuser_password" ]; then
      DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
    else
      DJANGO_SUPERUSER_PASSWORD='admin'
    fi
  fi

python3 /opt/digimenu/manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='${DJANGO_SUPERUSER_NAME}'):
  u=User.objects.create_superuser('${DJANGO_SUPERUSER_NAME}', '${DJANGO_SUPERUSER_MAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
END
  echo "Superuser Username: ${DJANGO_SUPERUSER_NAME}, E-mail: ${DJANGO_SUPERUSER_MAIL}"
fi


# run python3 manage.py cto compilescss
#python3 /opt/digimenu/manage.py compilescss
# run python3 manage.py collectstatic
# python3 /opt/digimenu/manage.py collectstatic --noinput

#move to digimenu directory
cd /opt/digimenu/

daphne -b digimenu -p 8080 myshop.asgi:application
