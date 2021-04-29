
# Team 9 Capacity checker 

Initial Requirements:
1. Clone the repository $ git clone https://github.com/swen-514-614-spring2021/term-project--team-9.git
2. Have AWS CLI and .aws/Credentials Set Up
3. Python verison 3.0+ installed https://www.python.org/downloads/



Project Set Up:

Install aws cdk
```
$ npm install -g aws-cdk
```
run $ cdk --version to test if you have cdk installed


Navigate to hello-cdk directory


To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

To manually create a virtualenv on Windows:

```
$ python -m venv .venv
```
If you are a Windows platform, you would activate the virtualenv like this:

```
% .\source.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

To Run Project:

```
$ cdk deploy HelloCdkStack --outputs-file .\frontend\src\cdk-outputs.json
```

Next you will need to commit, add, and push to the repo to trigger the amplify build in the aws build
```
$ git add .
$ git commit -m "pushing api gateway"
$ git push
```

Next you will need to set up the database and enter your phone number in the format(i.e. python createschema.py +14089214831)

```
$ python createschema.py <enterphonenumber>
```

Last Step, you will need to run the python script that connects to wegmans parking cam(https://www.youtube.com/watch?v=oIBERbq2tLA)

```
python stream.py
```

To access the frontend front go the link outputted after the cdk deploy is finished running

```
$ i.e. HelloCdkStack.frontend = https://main.d2g78g2grhl4ny.amplifyapp.com
```

#Shutting Everything down

```
$ cdk destroy
```

#Notes
Sometime the S3 does not like the file name, so you will need to cdk destroy and deploy again 