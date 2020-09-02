FROM ubuntu:bionic
LABEL maintainer="github.com/JamesWRC"

#   Update system.
RUN apt-get update

#   Install Python and pip.
RUN apt-get -y install python3 && apt-get -y install python3-pip

#   Install required Python libraries
RUN pip3 install requests && pip3 install Flask && pip3 install SQLAlchemy

#   Copy code across
ADD ./codebase /codebase

#   Give app andscripts permissions to run in the container.
RUN chmod +x /codebase/app.py
RUN chmod +x /codebase/entrypoint.sh
RUN chmod +x /codebase/runner.sh


#   Expose local web server port (80)
EXPOSE 80

# Run tests (-u = unbuffered so user can see testing / amy errors)
RUN ["python3","-u","/codebase/testRunner.py"]

# run the server
CMD /codebase/entrypoint.sh
