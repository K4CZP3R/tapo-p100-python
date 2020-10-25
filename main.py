from logger import Logger
from p100 import P100

log = Logger("main")

my_bulb = P100("192.168.137.13")
my_bulb.handshake()
my_bulb.login_request("TPLINKEMAIL", "TPLINKPASSWORD")
my_bulb.change_state(True, "88-00-DE-AD-52-E1")