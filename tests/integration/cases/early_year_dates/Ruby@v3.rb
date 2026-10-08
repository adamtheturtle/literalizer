require 'date'
my_data = {
  "date" => Date.new(99, 5, 27),
  "naive" => Time.utc(1, 1, 1, 12, 30, 0),
  "recent" => Time.utc(2024, 5, 27, 10, 0, 0),
}
