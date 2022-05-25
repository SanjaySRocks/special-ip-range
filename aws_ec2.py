import boto3
import time
import logging
import discordalert

COOLDOWN = 30

""" Initialize """
session = boto3.Session(profile_name='sanjaycs')
client = session.client('ec2')


""" Logging """
logging.basicConfig(filename='ec2.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(lineno)d | %(message)s')
# logging.disable()

""" Return true if its a special ip range """
def isSpecial(ip):
    ip_exploded = ip.split('.')
    
    if(ip_exploded[2] == ip_exploded[3]):
        return True

    return False


""" Main function assign ip Address and checks if its special """
def CreateStaticIP():
    while True:

        response = client.allocate_address()
        logging.info('Create IP Status: {}'.format(response['PublicIp']))

        if response['PublicIp']:
            ip_address = response['PublicIp']
            allocation_id = response['AllocationId']

            logging.info('Created Static IP: {}'.format(ip_address))
            print(ip_address)
            
            if isSpecial(ip_address):
                logging.info("Special IP Found: {}".format(ip_address))
                discordalert.AlertDiscord('{} we found it :D'.format(ip_address))
                break
            else:
                release_static_ip = client.release_address(AllocationId=allocation_id)
                logging.info('Delete IP Status: {}'.format(release_static_ip))

            time.sleep(int(COOLDOWN))

        else:
            break
        


if __name__ == "__main__":
    CreateStaticIP()