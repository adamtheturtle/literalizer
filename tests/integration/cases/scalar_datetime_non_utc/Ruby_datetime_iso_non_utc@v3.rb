my_data = "2024-01-15T18:00:00+05:30"
# Independent native value checks.
case "ISO"
when "EPOCH"
  raise "epoch value or type changed" unless my_data.instance_of?(Integer) && my_data == 1705321800
when "ISO"
  raise "ISO value or type changed" unless my_data.instance_of?(String) && my_data == "2024-01-15T18:00:00+05:30"
when "RUBY"
raise "datetime type changed" unless my_data.instance_of?(Time)
raise "datetime instant changed" unless my_data.to_r == Rational(1705321800000000, 1000000)
raise "datetime offset changed" unless my_data.utc_offset == 19800
else
  raise "unchecked datetime representation"
end
