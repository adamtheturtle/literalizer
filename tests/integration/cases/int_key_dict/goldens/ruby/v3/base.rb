my_data = {
  1 => "one",
  2 => "two",
  42 => "answer",
}
# Independent native value checks.
raise "mapping keys or values changed" unless my_data == {1 => "one", 2 => "two", 42 => "answer"}
raise "mapping key type changed" unless my_data.keys.all? { |key| key.instance_of?(Integer) }
