my_data = [
  5.0e-324,
  2.2250738585072014e-308,
  1.0e-307,
  1.0e21,
  -1.5e300,
  1.7976931348623157e308,
  -1.7976931348623157e308,
]
# Independent native value checks.
raise "float type changed" unless my_data.all? { |value| value.instance_of?(Float) }
raise "float precision or sign changed" unless my_data.map { |value| [value].pack("G").unpack1("H*") } == ["0000000000000001", "0010000000000000", "0031fa182c40c60d", "444b1ae4d6e2ef50", "fe41eb2d66005835", "7fefffffffffffff", "ffefffffffffffff"]
