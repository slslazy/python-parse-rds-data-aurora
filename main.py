import boto3

rds_client= boto3.client('rds-data')
db_arn = ''
secret_arn = ''
db_name = ''

def main( event, context ):
    return return_content( exec_sql( 'select * from some_table limit 50' ) )

#####################################################
################# Helper Functions ##################
#####################################################

#####################################################
# Execute SQL
#####################################################
def exec_sql( sql ):
    try:
        response = rds_client.execute_statement(
            resourceArn = db_arn,
            secretArn = secret_arn,
            database = db_name,
            includeResultMetadata = True,
            sql = sql)
        data_values = []
        for record in response['records']:
            row_data = {}
            index = 0
            for data_dict in record:
                for data_type, data_value in data_dict.items():
                    print(data_type, data_value)
                    row_data[response['columnMetadata'][index]['name']] = data_value
                    index += 1
            data_values.append(row_data)
        response = data_values
    except BaseException as e:
        response = str(e)
    return response

#####################################################
# Handle Return Content
#####################################################
def return_content( data ):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps( data, indent=4, sort_keys=True )
    }