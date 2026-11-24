my_data = [
  -0.0,
  1.5,
]
# Independent native value checks.
raise "float type changed" unless my_data.all? { |value| value.instance_of?(Float) }
raise "float precision or sign changed" unless my_data.map { |value| [value].pack("G").unpack1("H*") } == ["8000000000000000", "3ff8000000000000"]
