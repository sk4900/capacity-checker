import boto3
import datetime
from datetime import timezone

s3 = boto3.resource('s3')
BUCKET = "bucketswen614"

filename = f"""GOL_2000_{datetime.datetime.now(timezone.utc)}"""

filename = filename.replace(" ", "____")

filename = filename.replace(":", "___") 

filename = filename.replace("+", "__") 

print(filename)


s3.Bucket(BUCKET).upload_file("group1.jpg", filename)

filename = filename.replace("____", " ")

filename = filename.replace("___", ":") 

filename = filename.replace("__", "+") 


print(filename)

filename = filename.split("_")

building = filename[0]

room = filename[1]

timestamp = filename[2]