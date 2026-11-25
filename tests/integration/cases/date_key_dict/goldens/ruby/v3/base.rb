require 'date'
my_data = {
  Date.new(2024, 1, 1, Date::GREGORIAN) => "new_year",
  Date.new(2024, 7, 4, Date::GREGORIAN) => "independence_day",
  Date.new(2024, 12, 25, Date::GREGORIAN) => "christmas",
}
# Independent native value checks.
raise "date key type changed" unless my_data.keys.all? { |key| key.instance_of?(Date) }
raise "date keys changed" unless my_data.map { |key, value| [key.iso8601, value] }.to_h == {"2024-01-01" => "new_year", "2024-07-04" => "independence_day", "2024-12-25" => "christmas"}
