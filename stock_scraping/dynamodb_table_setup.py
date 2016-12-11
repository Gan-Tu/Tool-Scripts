'''
This script helps you setup a DynamoDB NoSQL table on AWS DynamoDB.

It assumes that you have necessary instructions setted up already for your
AWS credentials, as well as boto3 library by AWS.
For more information, check out AWS offical documentation online.
@author Gan Tu
@version python 3
'''

import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='stock-v1',
    KeySchema=[
        {
            'AttributeName': 'symbol',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'timestamp',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'symbol',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'timestamp',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
# Feel free to change the table name.
table.meta.client.get_waiter('table_exists').wait(TableName='stock-v1')

print("table created.")
