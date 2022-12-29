# csv-transactions
Credit and Debit Operations, Send via Mail

### Requirements
* Docker
* docker-compose
* AWS CLI

### Setup

**_Main terminal_**

`$ docker-compose up --build`
> With this command we will be to raise the images and containers related to the project

> The Terminal listens dor the events that will arrive at the initialized service

**_At another terminal:_**

`$ curl -XPOST "http://127.0.0.1:9000/2015-03-31/functions/function/invocations" -d "{}"`

> You can invoke the lambda function this way or use an API client