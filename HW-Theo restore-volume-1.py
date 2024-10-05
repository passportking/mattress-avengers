'''we want to recover the latest working state of the EC2 instance by creating a new volume from the snapshot 
and then attaching that volume to that ec2 instance so that it can continue running.
'''

import boto3
from operator import itemgetter



ec2_client = boto3.client('ec2', region_name="eu-west-2")
ec2_resource = boto3.resource('ec2', region_name="eu-west-2")

#The existing instance id for dev that we want to 
#do a recovery on. we make the assumption that the 
#instance only has 1 volume

instance_id = "i-0dcd30b532b6fd7a1"

'''
We want to get the snapshots that were created for 1 volume associated with this instance. For that we need to get the volumes
of that instance, then get the snapshots for that volume.
'''

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]

        }


    ]
)

'''
Here we pass in the filter to give us the volumes that are attached to the
above filter id

'''


instance_volume = volumes['Volumes'][0]

'''
Here were grabbing the first element from the list because were expecting the list to only have 1 element.
'''


#print(instance_volume)

'''This should be the volume attached to the instance
Now we want to get the snapshots for that volume assuming that is the volume that is corrupt.
#So we want to grab the latest snapshot of that volume to recover that instance
'''

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]

        }
    ]
)

'''
We are looking for our own snapshots and then we have the filters 
which basically sets the volume id that the snapshot belongs to
returns all the snapshots that were created from the volume attached to dev

'''

latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse = True)[0]

print(latest_snapshot['StartTime'])


'''
Now we have the latest snapshot, we created a new volume from that snapshot
Then we attached that that volume to our instance.
'''

new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="eu-west-2a",
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value':'dev'
                
                }
            ]
        }
    ]
)




while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])#This will give us the volume we created and on that volume we have state which basically contains info about state, whether its available, is it creating etc.
    print(vol.state)#Here the state is printed
    if vol.state == 'available':#If the volume state is available so not creating any more then we want to execute the logic below
        ec2_resource.Instance(instance_id).attach_volume(
    VolumeId=new_volume['VolumeId'],
    Device='/dev/xvdb'
    )
    break


'''
Here we check the state of the volume until it becomes available using a while loop
#every time we go through an iteration with the while loop we get the new state of the volume
in oreder to kill the forever while loop we use break

'''

'''
For our volume to be able to attach to an instance it has to be in an available
state. First it's in creation state then available, then we can attach it to an instance
When we execute we see the error message that the volume is not in the available state.
its still in the creating state. Its just a couple of milliseconds before it changes to 
available as can be seen on the UI. So we have an extra dev volume got created now in the available state.
But right at the time we executed this function it was not in the available state
'''

'''
To fix the timing issue problem between the two functions execution 
we want to wait just a little bit to allow the volume to get created and become available,
and then try and attach that volume
'''