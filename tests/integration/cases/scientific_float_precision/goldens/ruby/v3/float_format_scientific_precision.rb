my_data = {
  "value" => 1.2345678901234567,
}
# Independent native value checks.
value = my_data.fetch("value")
raise "float precision changed" unless value.instance_of?(Float) && [value].pack("G").unpack1("H*") == "3ff3c0ca428c59fb"
