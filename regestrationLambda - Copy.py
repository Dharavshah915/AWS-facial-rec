import boto3 #used to call AWS Services


s3 = boto3.client("s3")
rekognition = boto3.client("rekognition", region_name = "ca-central-1")
dynamodbTableName = "employee"
dynamodb = boto3.resource("dynamodb", region_name = "ca-central-1")
employeeTable = dynamodb.Table(dynamodbTableName)


def lambda_handler(event, context): #triggered by s3 bucket and the bucket name and the file name wll bein the event object
    print(event) # incase of errors
    bucket = event["Records"][0]["s3"]["bucket"]["name"] #bucket name
    key = event["Records"][0]["s3"]["object"]["key"] # image name of employee
    
    try: # indexing image
        response = index_employee_image(bucket, key)
        print(response) 
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:#website 's server sends to the browser to indicate whether or not that request can be fulfilled 200 means success
            faceId = response["FaceRecords"][0]["Face"]["FaceId"] # used to identify people
            name = key.split(".")[0].split("_") # firstname_lastname.jpeg
            firstName = name[0]
            lastName = name[1]
            register_employee(faceId, firstName, lastName)
        return response
    except Exception as e:
        print(e)
        print("Error")
        raise e
        
        
def index_employee_image(bucket, key):
    response = rekognition.index_faces(
    Image = {
        "S3Object":
        {
            "Bucket": bucket,
            "Name": key
        }
    },
    CollectionId = "employees" 
    )
    return response
def register_employee(faceId, firstName, lastName):
    employeeTable.put_item(
    Item = {
        "rekognitionId" : faceId,
        "firstname" : firstName,
        "lastName" : lastName
    }
    )
