require 'date'
my_data = [
  Date.new(2024, 1, 15, Date::GREGORIAN),
  Date.new(2024, 2, 20, Date::GREGORIAN),
]
# Independent native value checks.
raise "date type changed" unless my_data.all? { |value| value.instance_of?(Date) }
raise "date values changed" unless my_data.map(&:iso8601) == ["2024-01-15", "2024-02-20"]
