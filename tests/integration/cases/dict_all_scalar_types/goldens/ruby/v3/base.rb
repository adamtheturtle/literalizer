require 'date'
my_data = {
  "s" => "string",
  "i" => 1,
  "f" => 1.5,
  "b" => true,
  "n" => nil,
  "d" => Date.new(2024, 1, 15, Date::GREGORIAN),
  "dt" => Time.utc(2024, 1, 15, 12, 0, 0),
  "by" => "48656c6c6f",
}
# Independent native value checks.
raise "record keys changed" unless my_data.keys.sort == ["s", "i", "f", "b", "n", "d", "dt", "by"].sort
raise "string changed" unless my_data["s"] == "string"
raise "integer changed" unless my_data["i"].instance_of?(Integer) && my_data["i"] == 1
raise "float changed" unless my_data["f"].instance_of?(Float) && my_data["f"] == 1.5
raise "boolean or null changed" unless my_data["b"] == true && my_data["n"].nil?
raise "date changed" unless my_data["d"].instance_of?(Date) && my_data["d"].iso8601 == "2024-01-15"
raise "datetime changed" unless my_data["dt"].instance_of?(Time) && my_data["dt"].to_r == 1705320000 && my_data["dt"].utc_offset == 0
raise "bytes changed" unless my_data["by"].instance_of?(String) && my_data["by"] == "48656c6c6f"
