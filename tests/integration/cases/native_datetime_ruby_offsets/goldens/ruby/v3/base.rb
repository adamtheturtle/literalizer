my_data = {
  "stamps" => [Time.new(2001, 2, 3, 4, 5, 6, 1), Time.new(2001, 2, 3, 4, 5, 6, -1), Time.new(2001, 2, 3, 4, 5, 6, Rational(1, 1000000)), Time.new(2001, 2, 3, 4, 5, 6, Rational(-1, 1000000)), Time.new(2001, 2, 3, 4, 5, 6, Rational(19815000001, 1000000)), Time.new(2001, 2, 3, 4, 5, 6, Rational(-19815000001, 1000000))],
}
# Independent native value checks.
offsets = [1000000, -1000000, 1, -1, 19815000001, -19815000001]
stamps = my_data.fetch("stamps")
raise "datetime count changed" unless stamps.size == offsets.size
stamps.zip(offsets).each do |stamp, offset|
  raise "datetime type changed" unless stamp.instance_of?(Time)
  raise "datetime offset changed" unless stamp.utc_offset == Rational(offset, 1000000)
  raise "datetime instant changed" unless stamp.to_r == Rational(981173106000000 - offset, 1000000)
end
