my_data = [
  9223372036854775807,
  9223372036854775808,
]
# Independent native value checks.
raise "integer type changed" unless my_data.all? { |value| value.instance_of?(Integer) }
raise "integer value changed" unless my_data == [9223372036854775807, 9223372036854775808]
