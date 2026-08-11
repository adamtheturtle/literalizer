require "set"
module Fixture_date_set_Crystal
extend self
my_data = Set{
    Time.utc(2024, 1, 15),
    Time.utc(2024, 6, 1),
}
end
