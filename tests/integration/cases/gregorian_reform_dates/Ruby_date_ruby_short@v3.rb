require 'date'
my_data = {
  "before_date" => Date.new(1582, 10, 4, Date::GREGORIAN),
  "gap_date" => Date.new(1582, 10, 10, Date::GREGORIAN),
  "transition_date" => Date.new(1582, 10, 15),
  "after_date" => Date.new(1582, 10, 16),
  "before_naive" => Time.utc(1582, 10, 4, 12, 30, 0 + Rational(1, 1000000)),
  "gap_naive" => Time.utc(1582, 10, 10, 12, 30, 0 + Rational(500000, 1000000)),
  "transition_positive" => Time.new(1582, 10, 15, 0, 30, 0, "+18:00"),
  "transition_negative" => Time.new(1582, 10, 15, 23, 30, 0, "-18:00"),
  "after_positive" => Time.new(1582, 10, 16, 0, 30, 0, "+18:00"),
}
