import digitalocean
import logging
import time

DigitalOceanToken = ""

COOLDOWN = 30

""" Logging """
logging.basicConfig(filename='digitalocean.log', filemode='w', level=logging.INFO, format='%(asctime)s | %(lineno)d | %(message)s')


""" Return true if its a special ip range """
def isSpecial(ip):
    ip_exploded = ip.split('.')
    
    if(ip_exploded[2] == ip_exploded[3]):
        return True

    return False


def CreateStaticIP():
    while True:
        floating_ip = digitalocean.FloatingIP(region_slug='blr1', token=DigitalOceanToken)

        static_ip = floating_ip.reserve()

        logging.info('Created Static IP: {}'.format(static_ip))
        print(static_ip)
        
        if str(static_ip):
            if isSpecial(str(static_ip)):
                logging.info("Special IP Found: {}".format(static_ip))
                break
            else:
                release_static_ip = floating_ip.destroy()
                
                if release_static_ip == True:
                    logging.info('Delete IP Status: {}'.format(release_static_ip))

            time.sleep(int(COOLDOWN))
            
        else:
            break



if __name__ == "__main__":
    CreateStaticIP()