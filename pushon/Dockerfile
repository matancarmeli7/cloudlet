FROM golang:1.13.4 as build-env
RUN mkdir /pushon
WORKDIR /pushon
COPY src/ .
RUN go mod download

CMD ["go","run","main.go"]
