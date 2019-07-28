FROM alpine/git AS cloner
RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/dbeltman/R510-Denoiser

FROM python:3 AS runner
# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app
ENV environment prod
# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP
# Expose the port uWSGI will listen on
EXPOSE 5000
# Copy the requirements file in order to install
# Python dependencies
COPY --from=cloner /app/R510-Denoiser/requirements.txt  .
# Install Python dependencies
RUN pip install -r requirements.txt
# We copy the rest of the codebase into the image
COPY --from=cloner /app/R510-Denoiser/ .
# Finally, we run uWSGI with the ini file we
# created earlier
CMD [ "uwsgi", "--ini", "app.ini" ]