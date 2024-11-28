import logging
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import serial

# Enable logging for pymodbus
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Test connection function
def test_connection():
    # Create ModbusSerialClient with correct parameters
    client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, timeout=1)

    # Try to connect to the Modbus device
    if client.connect():
        print("Connection successful!")
        client.close()
    else:
        print("Connection failed.")

# Test if the serial library is available
try:
    import serial
    print("Serial module imported successfully!")
    test_connection()
except ImportError as e:
    print("Error: Serial module is not installed or not working.")
    print(e)
