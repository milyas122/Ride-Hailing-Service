# Safeer Backend Hiring Project
## Installation
- Click this link to download [Python](https://www.python.org/downloads/)
- Download and install [Node Js](https://nodejs.org/en/)
- Download and run the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) MSI installer

Install the serverless CLI via NPM:

```bash
npm install -g serverless
```
Once AWS CLI is installed, configure AWS CLI with AWS Access Key ID and AWS Secret Access Key.
```bash
 aws configure
```

First, create Python virtual environment for packages installation *(Windows OS)*

```bash
python -m venv env
```
Once created activate it through the below command *(Windows OS)*

```bash
env\scripts\activate
```
Install all python requirements via PIP 

```bash
pip install -r requirements.txt
```
Install node modules via NPM

```bash
npm i
```

## Add Google API KEY
Find Google API Key in your email. Replace this provided API Key (Or your Own Google API Key) in serverless.yaml under function section and in Trip function replace <API-Key> with original one.


```yaml
functions:
  TripFare:
    handler: src/api/trip_fare.lambda_handler
    layers:
      - Ref: PythonRequirementsLambdaLayer
    environment:
      API_KEY: <API-Key> # Its for demo purpose, In real case all envrionment variables are in seperate file which is not a part of git repository
    package:
      patterns: 
        - ./src/api/trip_fare.py
    iamRoleStatementsName: TripFare-policy-sls-${self:provider.region}-${self:provider.stage}
    events:
      - http:
          path: trip/fare
          method: get
          cors: True
```

## After Successful Installation uses the below to deploy serverless code to AWS.  

```bash
serverless deploy 
```

## Once successfully deploy its time to test APIs, so follow below steps to achive this

1. Use this link to get APIs collection. 
   https://www.getpostman.com/collections/853aa642ec5ec96cfdc8
2. After this set **baseUrl** environment variable to your one.
  
---
*NOTE*

In Case, there is any issue in deploy or other, use these below APIs in Postman to rate my assignment.
 1. GET - https://mvfll0wvx5.execute-api.us-east-1.amazonaws.com/dev/trip/fare
 2. POST - https://mvfll0wvx5.execute-api.us-east-1.amazonaws.com/dev/trip/create
 3. POST - https://mvfll0wvx5.execute-api.us-east-1.amazonaws.com/dev/trip/{tripId}/complete
 4. GET - https://mvfll0wvx5.execute-api.us-east-1.amazonaws.com/dev/trips/complete

---
