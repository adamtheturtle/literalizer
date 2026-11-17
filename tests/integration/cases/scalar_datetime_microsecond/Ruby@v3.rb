my_data = Time.utc(2024, 1, 15, 12, 30, 0 + Rational(123456, 1000000))
# Independent native value checks.
raise "datetime type changed" unless my_data.instance_of?(Time)
raise "datetime instant changed" unless my_data.to_r == Rational(1705321800123456, 1000000)
raise "datetime offset changed" unless my_data.utc_offset == 0
