FROM nginx:stable-alpine

#remove the default conf
RUN rm /etc/nginx/conf.d/default.conf

COPY ./apps/docker/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

# Copy static files from the backend build
# COPY ../../backend/static /apps/backend/static

# Copy static files from the frontend build
COPY ./apps/frontend/dist /usr/share/nginx/html

# Expose port 80 and 443
EXPOSE 80 443

CMD [ "nginx-debug", "-g", "daemon off;" ]