my_data = [
  5.0e-324,
  -5.0e-324,
  2.2250738585072014e-308,
]
# Independent native value checks.
raise "float type changed" unless my_data.all? { |value| value.instance_of?(Float) }
raise "float precision or sign changed" unless my_data.map { |value| [value].pack("G").unpack1("H*") } == ["0000000000000001", "8000000000000001", "0010000000000000"]
