FROM php:8-apache

RUN set -x && \
  apt-get -y update && \
  apt-get install -y libicu-dev unzip git postgresql-server-dev-all && \
  NPROC=$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1) && \
  docker-php-ext-install -j${NPROC} intl && \
  docker-php-ext-install -j${NPROC} pdo_pgsql && \
  docker-php-ext-install -j${NPROC} pdo_mysql && \
  rm -rf /tmp/pear

  # Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /app

COPY composer.json composer.json
#COPY composer.lock composer.lock

ENV COMPOSER_ALLOW_SUPERUSER=1

RUN composer install \
    --no-interaction \
    --no-plugins \
    --no-scripts \
    --no-dev \
    --prefer-dist

RUN composer dump-autoload