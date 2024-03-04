FROM gradle:jdk17 

WORKDIR /usr/src/app
COPY ./src .
RUN gradle build
    
EXPOSE 8080
CMD ["gradle", "bootRun"]
