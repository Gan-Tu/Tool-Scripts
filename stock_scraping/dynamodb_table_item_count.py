'''
This script helps you count the number of items stored in the
DynamoDB NoSQL table you specified on your AWS DynamoDB.

It assumes that you have necessary instructions setted up already for your
AWS credentials, as well as boto3 library by AWS.
For more information, check out AWS offical documentation online.
@author Gan Tu
@version python 3
'''

import boto3

client = boto3.client('dynamodb')

# Feel free to change the table name to your targeted table.
response = client.describe_table(TableName='stock-v1')

count = str(response['Table']['ItemCount'])

print("Total item count is: " + count)