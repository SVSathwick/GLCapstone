import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import random
import datetime
import sched

# Define ENDPOINT, TOPIC, RELATOVE DIRECTORY for CERTIFICATE AND KEYS
ENDPOINT = "ayis9dea5ktp8-ats.iot.us-east-1.amazonaws.com"
PATH_TO_CERT = "..\\config"
TOPIC = "iot/agritech"

SPRIKLER_LOCATION_LIST = list()
SENSOR_LIST = list()

# AWS class to create number of objects (devices)
class AWS():
    # Constructor that accepts client id that works as device id and file names for different devices
    # This method will obviosuly be called while creating the instance
    # It will create the MQTT client for AWS using the credentials
    # Connect operation will make sure that connection is established between the device and AWS MQTT
    def __init__(self, client, certificate, private_key, sprinkler):
        self.client_id = client
        self.device_id = client
        self.sprinkler = sprinkler
        self.cert_path = PATH_TO_CERT + "\\" + certificate
        self.pvt_key_path = PATH_TO_CERT + "\\" + private_key
        self.root_path = PATH_TO_CERT + "\\" + "AmazonRootCA1.pem"
        self.myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(self.client_id)
        self.myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(self.root_path, self.pvt_key_path, self.cert_path)
        self._connect()

    # Connect method to establish connection with AWS IoT core MQTT
    def _connect(self):
        self.myAWSIoTMQTTClient.connect()

    # This method will publish the data on MQTT 
    # Before publishing we are confiuguring message to be published on MQTT
    def publish_soil_data(self):
        print('Begin Publish')
        for i in range (10):
            message = {}    
            value = float(random.normalvariate(99, 1.5))
            value = round(value, 1)
            timestamp = str(datetime.datetime.now())
            message['deviceid'] = self.device_id
            message['timestamp'] = timestamp
            message['sprinkler'] = self.sprinkler
            message['datatype'] = 'Temperature'
            message['value'] = value
            messageJson = json.dumps(message)
            self.myAWSIoTMQTTClient.publish(TOPIC, messageJson, 1) 
            print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
            time.sleep(0.1)
        print('Publish End')

    # Disconect operation for each devices
    def disconnect(self):
        self.myAWSIoTMQTTClient.disconnect()

# Main method with actual objects and method calling to publish the data in MQTT
# Again this is a minimal example that can be extended to incopporate more devices
# Also there can be different method calls as well based on the devices and their working.
if __name__ == '__main__':
    
    #Reading the configuration file
    f = open('sprinkler_config_2.json', 'r')
    config = json.loads(f.read())
    f.close()

    sensors = []

    sprinklers = config['sprinklers']
    for sprinkler in sprinklers:
        # print(f'type: {type(sprinkler)}')
        # print(sprinkler)

        lat = sprinkler['lat']
        lon = sprinkler['lon']

        # Map Sprinkler with location coordinates
        sprinklr_loc_map = { 'sprinkler':sprinkler['name'], 'lat':lat, 'lon':lon}
        SPRIKLER_LOCATION_LIST.append(sprinklr_loc_map)
        
        #sprinkler_name = sprinkler['name']
        #print(f'sprinkler: {sprinkler_name}, lon: {lon}, lat: {lat}')

        cert = sprinkler['certificate']
        private_key = sprinkler['private_key']
        sensors = sprinkler['soil_sensors']

        for dev_id in sensors:
            #print(f'device id: {dev_id}')
            #print(f'Certificate: {cert}')
            #print(f'priate key: {private_key}')

            # Create SOil sensor device Objects and add them to SENSOR_LIST
            sensor = AWS(client=dev_id, certificate=cert, private_key=private_key, sprinkler=sprinkler['name'])
            SENSOR_LIST.append(sensor)

    #print('SPRIKLER_LOCATION_LIST')
    for item in SPRIKLER_LOCATION_LIST:
        print(item)
    
    print('')

    #print('SENSOR_LIST')
    #publish soil data for each sensor
    for sensor in SENSOR_LIST:
        sensor.publish_soil_data()