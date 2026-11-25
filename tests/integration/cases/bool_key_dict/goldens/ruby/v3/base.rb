my_data = {
  true => "yes",
  false => "no",
}
# Independent native value checks.
raise "mapping keys or values changed" unless my_data == {true => "yes", false => "no"}
