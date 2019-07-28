FROM alpine/git AS cloner
RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/dbeltman/R510-Denoiser


FROM nginx:latest
EXPOSE 80

COPY --from=cloner /app/R510-Denoiser/app.conf /etc/nginx/conf.d