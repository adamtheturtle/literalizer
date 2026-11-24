my_data = {
    "value": 1.2345678901234567,
}
# Independent native value checks.
import struct
assert type(my_data["value"]) is float
assert struct.pack("!d", my_data["value"]).hex() == "3ff3c0ca428c59fb"
