FROM golang:1.13.4-alpine as build-env
RUN mkdir /pushon
WORKDIR /pushon
COPY src/ .
RUN go mod download
RUN go build -o pushon

FROM alpine:latest
RUN mkdir /pushon
WORKDIR /pushon
RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*
COPY --from=build-env /pushon/ .

CMD ["./pushon"]
