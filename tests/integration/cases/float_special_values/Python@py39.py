my_data = (
    float("inf"),
    float("-inf"),
    float("nan"),
)
# Independent native value checks.
import math
assert all(type(value) is float for value in my_data)
assert len(my_data) == 3
assert math.isinf(my_data[0]) and my_data[0] > 0
assert math.isinf(my_data[1]) and my_data[1] < 0
assert math.isnan(my_data[2])
