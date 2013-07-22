from pybonjourutil import *


username = raw_input("Username: ")
status = "Online"





register(username,"_chat._tcp.",1337)


browse_resolve_query("_chat._tcp.")