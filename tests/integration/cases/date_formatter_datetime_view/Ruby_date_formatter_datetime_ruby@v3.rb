require 'date'
my_data = {
  "ancient" => Date.new(1500, 3, 1, Date::GREGORIAN),
  "reform_gap" => Date.new(1582, 10, 10, Date::GREGORIAN),
  "reform_day" => Date.new(1582, 10, 15, Date::GREGORIAN),
  "modern" => Date.new(2024, 1, 15, Date::GREGORIAN),
  "ancient_date" => Date.new(1500, 3, 1, Date::GREGORIAN),
  "reform_gap_date" => Date.new(1582, 10, 10, Date::GREGORIAN),
  "reform_day_date" => Date.new(1582, 10, 15, Date::GREGORIAN),
  "modern_date" => Date.new(2024, 1, 15, Date::GREGORIAN),
}
expected = {
  "ancient" => [1500, 3, 1],
  "reform_gap" => [1582, 10, 10],
  "reform_day" => [1582, 10, 15],
  "modern" => [2024, 1, 15]
}
expected.each do |field, parts|
  wanted = Date.new(parts[0], parts[1], parts[2], Date::GREGORIAN)
  actual = my_data.fetch(field)
  date_value = my_data.fetch("#{field}_date")
  raise "incorrect Gregorian date for #{field}" unless actual == date_value && actual == wanted
end
