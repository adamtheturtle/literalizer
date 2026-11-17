my_data = (
    -0.0,
    1.5,
)
# Independent native value checks.
import struct
assert isinstance(my_data, (list, tuple))
assert all(type(value) is float for value in my_data)
assert [struct.pack("!d", value).hex() for value in my_data] == ['8000000000000000', '3ff8000000000000']
