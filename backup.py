import time
import os
import boto3

# Purpose: This is a simple Python Tool to automate backing up your
# Apiary.io files.  Note, will still need to upload the Apiary CLI via
# Ruby Gems.

# You can get your API token here: https://login.apiary.io/tokens
APIARY_API_KEY = YOUR_API_KEY

bucket = YOUR_BUCKET
s3 = boto3.resource('s3',
  aws_access_key_id = ACCESS_KEY,
  aws_secret_access_key = SECRET_KEY
)

apis = [
  "your_api_name",
]

# Variables used to count and store the dates.
datestamp = str(time.strftime("%Y%m%d_"))
year = str(time.strftime("%Y"))
month = str(time.strftime("%m"))
day = str(time.strftime("%d"))
counter = 0

# A mix of command line arguements, uploading to S3, and removing local files.
for api in apis:
  apiary_cli_command =  "apiary fetch --api-name="+'"'+api+'"'+ ' --output="'+datestamp+api+'.apib'+'"'

  #Optional Output used to see progress.  Very helpful.
  print "calling " + apiary_cli_command
  os.system("export APIARY_API_KEY="+APIARY_API_KEY+";"+apiary_cli_command)

  data=""
  with open(datestamp+api+'.apib', 'r') as myfile:
    data=myfile.read()
  os.remove(datestamp+api+'.apib')
  s3.Bucket(bucket).put_object(Key=year+'/'+month+'/'+day+'/'+datestamp+api+'.apib', Body=data)
  counter = counter +1;

#Optional Output
print "Done writing this many files to s3: " + str(counter)
print "Check the S3 Drive here: " + 'https://s3.amazonaws.com'+'/'+bucket+'/'+year+'/'+month+'/'+day+"/"
