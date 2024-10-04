#cleanup-snapshots.py

#imports the library
import boto3

#imports the operator module that acts as helper used for sorting and creating a ec2 client.

from operator import itemgetter


# which the script then calls on the ec2 client

ec2_client = boto3.client('ec2', region_name="us-east-1")

#method on the EC2 client. It's looking for snapshots owned by the current AWS account (specified by the ownerid named 'self) 
#'self' is a special value that means the current AWS account
#the snapshots are then sorted by the 'StartTime' key in descending order using the 'sorted' function 
#and the 'itemgetter' function from the 'operator' module.

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'])

sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True) #reverse=true changes the ascend order of the start time you grabbed. 
#if you dont change the order the newest snaps will be at the top.

#the script then prints the 'StartTime' value for each snapshot in the sorted list in the Bash command terminal.
#sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

for snap in snapshots['Snapshots']:
    print('###########')

    for snap in sorted_by_date:
        print(snap['StartTime'])


# this the finial code which you would leave the above two for loops out. the above was only to view your snaps.

import boto3 #Is a Software development Kit that allows Python to configure in the AWS platform.

from operator import itemgetter # operator allows you to utilize itemgetter.  

ec2_client = boto3.client('ec2', region_name="us-east-1") # ec2_client is how you will identify your AWS account.

snapshots = ec2_client.describe_snapshots( #you will be asked the OwnerId because there are 3 types. (Self)which is you, (AWS)AWS saves snapshots in the background &
   OwnerIds=['self']) # and the last is (AccountId)

sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True) #itemgetter allows you to access the dictionary where StartTime can be accessed

for snap in sorted_by_date[2:]: # the number 2 identifies that I want to keep the 1st 2 values and delete the rest.
    response = ec2_client.delete_snapshot(  # is you telling it the action you expect.
        SnapshotId=snap['SnapshotId'] 
    )
    print(response)

      
