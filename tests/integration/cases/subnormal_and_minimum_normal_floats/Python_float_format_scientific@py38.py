my_data = (
    5.0e-324,
    -5.0e-324,
    2.2250738585072014e-308,
)
# Independent native value checks.
import struct
assert all(type(value) is float for value in my_data)
assert [struct.pack("!d", value).hex() for value in my_data] == ['0000000000000001', '8000000000000001', '0010000000000000']
