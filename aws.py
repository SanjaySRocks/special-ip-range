import boto3
import time
import logging
import discordalert

COOLDOWN = 30

""" Initialize """
session = boto3.Session(profile_name='sanjaycs')
client = session.client('lightsail')


""" Logging """
logging.basicConfig(filename='lightsail.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(lineno)d | %(message)s')
# logging.disable()

""" Return true if its a special ip range """
def isSpecial(ip):
    ip_exploded = ip.split('.')
    
    if(ip_exploded[2] == ip_exploded[3]):
        return True

    return False


""" Main function assign ip Address and checks if its special """
def CreateStaticIP():
    import uuid
    random_hash = str(uuid.uuid4())[:5]
    ipName='static-ip-{}' .format(random_hash)

    while True:

        response = client.allocate_static_ip(
            staticIpName=ipName
        )
        
        logging.info('Create IP Status: {}'.format(response['operations'][0]['status']))

        if response['operations'][0]['status'] == 'Succeeded':

            static_ip = client.get_static_ip(staticIpName=ipName)
            ip_address = static_ip['staticIp']['ipAddress']

            logging.info('Created Static IP: {}'.format(ip_address))
            print(ip_address)
            
            if isSpecial(ip_address):
                logging.info("Special IP Found: {}".format(ip_address))
                discordalert.AlertDiscord('{} we found it :D'.format(ip_address))
                break
            else:
                release_static_ip = client.release_static_ip(staticIpName=ipName)
                logging.info('Delete IP Status: {}'.format(release_static_ip['operations'][0]['status']))

            time.sleep(int(COOLDOWN))

        else:
            break
        


if __name__ == "__main__":
    CreateStaticIP()