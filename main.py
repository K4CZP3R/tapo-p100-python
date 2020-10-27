
from p100 import P100
import logging
import argparse

parser = argparse.ArgumentParser(description="Change plug state.")
parser.add_argument('tplink_email', metavar='TPLINK_EMAIL', type=str, help="Your TPLink account email")
parser.add_argument('tplink_password', metavar='TPLINK_PASS', type=str, help="Your TPLink account password")
parser.add_argument('address', metavar='ADDR', type=str, help="Address of your plug (ex. 192.168.2.22)")
parser.add_argument('new_state', metavar='STATE', type=int, help="New state of the plug (on=1 off=0) ")


args = parser.parse_args()


logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

logger.info(f"Will change state of plug at '{args.address}' to '{args.new_state}'")

my_bulb = P100(args.address)
my_bulb.handshake()
my_bulb.login_request(args.tplink_email, args.tplink_password)
my_bulb.change_state(args.new_state, "88-00-DE-AD-52-E1")

# Now if the plug is on
is_plug_on = my_bulb.is_on()
logger.info(f"Returned result: {is_plug_on}")
