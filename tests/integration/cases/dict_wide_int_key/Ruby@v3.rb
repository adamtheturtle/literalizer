my_data = {
  99999999999999999999999999 => "tag",
}
# Independent native value checks.
raise "mapping keys or values changed" unless my_data == {99999999999999999999999999 => "tag"}
raise "mapping key type changed" unless my_data.keys.all? { |key| key.instance_of?(Integer) }
