'''
Library of codes, it allows Amazon AWS to communicate with our programs
'''
import boto3
import schedule



ec2_client = boto3.client('ec2', region_name="eu-west-2")

'''
ec2_client = boto3.client('ec2', region_name="eu-west-2")

Dependent on your own region

This line tells us where and what we're doing in AWS. The what is the ec2 
service and the where is the region. Change region to be in the same region as ec2 instances created
every time we use bot03 were going to use this line or somewhat similar line if were interacting with any ec2 service
So what it does is it initialises the EC2 client thats basically a part of boto3 that lets you talk to EC2 in AWS
and as we can see it also specifies the region.
that were gonna be working with
'''

'''
volumes = ec2_client.describe_volumes()

This line allows AWS to list the volumes and describe all the volumes in a specified region
#It initialises a list called volumes. On the right side It calls the ec2_client that we made 
in the previous line. And then it uses the ec2 client to call the built in function from boto3 called describe volumes.
And then it contacts AWS. And it says hey in the ec2 service in this region I want to know about all the volumes and I want all that information.
And then the ec2 client gets it and then it brings it back to our computer and then loads it into our volumes list
And so all the information about the volumes of the ec2s are loaded into that list called volumes.
'''

'''
We defined our create_volume_snapshots


Filters=[
    {
        'Name': 'tag:Name',
        'Values': ['dev']
    }

Our filter matches all the volumes that has name dev. It's how we set the filters based on tag.
Filters out the dev volume and only creates snapshots only for the dev volumes. We only want to create snapshots of our dev server 
We create filters of the volume we only want to create snapshots on so basically in describe volumes specify that we only want 
the dev servers.

'''

def create_volume_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[ #our filter has matches all the volumes that has name dev. It's how we set the filters based on tag
            {#filters out the dev volume and only creates snapshots only for the dev volumes
                'Name': 'tag:Name',
                'Values': ['dev']
            }
        ]
    )        
    for volume in volumes['Volumes']:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId']
        )
        print(new_snapshot)
        


schedule.every(20).seconds.do(create_volume_snapshots)

while True:
    schedule.run_pending()

'''
Here we add a scheduler for our scheduled backup from our scehdule library
above. We basically set the schedule for snapshots for every 20 seconds.
Basically we tell our scheduler to execute cretate_volume_snapshots
function every 20 seconds. To test it will exeecute
and check snapshots in UI. Remember that it only filters the dev volume as above
'''



#prints the list of volumes
#print(volumes['Volumes'])

#$ python ./voulume-backups.py This command that we put in is telling us to activate the code above