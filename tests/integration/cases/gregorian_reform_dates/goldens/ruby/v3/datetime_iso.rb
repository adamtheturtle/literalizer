require 'date'
my_data = {
  "ancient_date" => Date.new(1500, 3, 1, Date::GREGORIAN),
  "modern_date" => Date.new(2024, 1, 15, Date::GREGORIAN),
  "before_date" => Date.new(1582, 10, 4, Date::GREGORIAN),
  "gap_date" => Date.new(1582, 10, 10, Date::GREGORIAN),
  "transition_date" => Date.new(1582, 10, 15, Date::GREGORIAN),
  "after_date" => Date.new(1582, 10, 16, Date::GREGORIAN),
  "before_naive" => "1582-10-04T12:30:00.000001",
  "gap_naive" => "1582-10-10T12:30:00.500000",
  "transition_positive" => "1582-10-15T00:30:00+18:00",
  "transition_negative" => "1582-10-15T23:30:00-18:00",
  "after_positive" => "1582-10-16T00:30:00+18:00",
}
