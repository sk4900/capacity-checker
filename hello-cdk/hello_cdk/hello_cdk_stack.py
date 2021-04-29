from aws_cdk import (
    core as cdk,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_sqs as sqs,
    aws_apigateway as apigw,
    aws_amplify as amp,
    aws_codebuild as cb
)
# from aws_cdk import aws_lambda_event_sources 

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk.aws_lambda_event_sources import SqsEventSource


import os.path
import os
dirname = os.path.dirname(__file__)


class HelloCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        S3policy =  iam.PolicyStatement(actions=['s3:*'],resources=['*'])
                    
        SQSpolicy = iam.PolicyStatement(actions=['sqs:*'],resources=['*'])
        
        Rekpolicy = iam.PolicyStatement(actions=['rekognition:*'],resources=['*'])

        rds_lambda_role = iam.Role(scope=self, id='cdk-lambda-role',
                                assumed_by =iam.ServicePrincipal('lambda.amazonaws.com'),
                                role_name='cdk-lambda-role',
                                managed_policies=[
                                iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaVPCAccessExecutionRole'),
                                iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaBasicExecutionRole')
                                ])
        policystatement = iam.PolicyStatement(
                    resources=["*"],
                    actions= ["sns:Publish"],
                    effect= iam.Effect.ALLOW
                    )

        token = cdk.SecretValue.plain_text("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")

        amplify_app = amp.App(self, "MyApp",
            source_code_provider=amp.GitHubSourceCodeProvider(
                owner="swen-514-614-spring2021",
                repository="term-project--team-9",
                oauth_token=token
            )
        )
        amplify_app.add_branch("main")

                    
        # matt beef bucket
        picbucket = s3.Bucket(self, "bucket1",
            bucket_name='bucketswen614',
            versioned=False,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True)


        # matt lambda
        fifosendfunction = _lambda.Function(self, "lambda_function1",
                                    code=_lambda.Code.asset(os.path.join(dirname, "send_to_fifo_queue")),
                                    runtime=_lambda.Runtime.PYTHON_3_7,                
                                    handler="lambda-handler.main",
                                    function_name="sendtofifoqueue")
        # remember to add role= to funciton
        fifosendfunction.add_to_role_policy(S3policy)
        fifosendfunction.add_to_role_policy(SQSpolicy)

        # notification for lambda to activate when file gets put into bucket
        notification = s3n.LambdaDestination(fifosendfunction)
        picbucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT, notification)


        # matt queue
        queueP = sqs.Queue(self, "Queue",
                          queue_name="picturequeue.fifo",
                          fifo=True,
                          content_based_deduplication=True)


        # matt lambda make it so this is activated by message sent to queue above then send it forward to bean bucket
        function_rekognition = _lambda.Function(self, "lambda_function2",
                                    code=_lambda.Code.asset(os.path.join(dirname, "send_to_rekognition")),
                                    runtime=_lambda.Runtime.PYTHON_3_7,                
                                    handler="lambda-handler.main",
                                    function_name="detect_labels")
        function_rekognition.add_to_role_policy(S3policy)
        function_rekognition.add_to_role_policy(SQSpolicy)
        function_rekognition.add_to_role_policy(Rekpolicy)

        event_source = function_rekognition.add_event_source(SqsEventSource(queueP))
        # event_source = functionbean.add_event_source(SqsEventSource(queueP))
        # event_source_id = event_source.event_source_id

        #VPC for RDS
        vpc = ec2.Vpc(self, "VPC", max_azs=2)

        #Sets password using secretmanageer
        password = cdk.SecretValue.plain_text("swen614Team9")

        #Creates RDS using POSTGRESQL
        myrds = rds.DatabaseInstance(
            self,
            "RDS",
            database_name="CCDatabase",
            engine= rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_12_5),
            instance_type= ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2,
                ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            storage_type=rds.StorageType.GP2,
            allocated_storage=20,
            credentials=rds.Credentials.from_password('team9',password),
            vpc_subnets={
                "subnet_type": ec2.SubnetType.PUBLIC
            } 
        )

        myrds.connections.allow_default_port_from_any_ipv4('5432')
        
        # FIFO Queue going into database
        queueDB = sqs.Queue(self, "DBQueue",
                          queue_name="dbqueue.fifo",
                          fifo=True,
                          content_based_deduplication=True)
                          
          
        # lambda for DB queue
        fifoDBsendfunction = _lambda.Function(self, "lambda_function3",
                                    code=_lambda.Code.asset(os.path.join(dirname, "send_to_db")),
                                    runtime=_lambda.Runtime.PYTHON_3_7,                
                                    handler="lambda-handler.main",
                                    role=rds_lambda_role,
                                    function_name="sendtodb",
                                    environment= {
                                            'DB_HOST': myrds.db_instance_endpoint_address
                                        }
                                    
                                    )    
        fifoDBsendfunction.add_to_role_policy(SQSpolicy)

        # attaches DBFIFO to the lambda                            
        event_source1 = fifoDBsendfunction.add_event_source(SqsEventSource(queueDB))

        # lambda for DB get 
        DBgetfunction = _lambda.Function(self, "lambda_function4",
                                    code=_lambda.Code.asset(os.path.join(dirname, "get_capacity_rds")),
                                    runtime=_lambda.Runtime.PYTHON_3_7,                
                                    handler="lambda-handler.main",
                                    role=rds_lambda_role,
                                    function_name="getfromdb",
                                    environment= {
                                            'DB_HOST': myrds.db_instance_endpoint_address
                                        }                                    
                                    )  

        DBgetfunction.add_to_role_policy(policystatement)


        api_gateway = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=DBgetfunction,
        )

        get_widgets_integration = apigw.LambdaIntegration(DBgetfunction,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api_gateway.root.add_method("GET", get_widgets_integration)   # GET /
        
 
        cdk.CfnOutput(self, 'frontend', value = "https://main."+amplify_app.default_domain)
        cdk.CfnOutput(self, 'rdsendpoint', value = myrds.db_instance_endpoint_address)


        
        
            

        
                            
