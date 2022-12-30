# csv-transactions
Credit and Debit Operations, Send via Mail

### Requirements
* Docker
* docker-compose
* AWS CLI

### Setup

**_Environment File_**

```
SENDER_MAIL="##ADD_MAIL##"
RECEIVER_MAIL="##ADD_MAIL##"
SENDER_PASS="##ADD_PASS##"
```
> First, Please copy and rename the env.dist file to .env

> After, Add the credentials and email that will receive the report


**_Main terminal_**

`$ docker-compose up --build`
> With this command we will be to raise the images and containers related to the project

> The Terminal listens dor the events that will arrive at the initialized service

**_At another terminal:_**

`$ curl -XPOST "http://127.0.0.1:9000/2015-03-31/functions/function/invocations" -d "{}"`

> You can invoke the lambda function this way or use an API client

**_Event to invoke the Lambda_**

`URL: http://127.0.0.1:9000/2015-03-31/functions/function/invocations`

`TYPE: POST`

```
{
	"operation": "BALANCE_REPORT",
	"user_uuid": "3dbc158a-4856-45c8-a329-fb26f7f9ec19"
}
```