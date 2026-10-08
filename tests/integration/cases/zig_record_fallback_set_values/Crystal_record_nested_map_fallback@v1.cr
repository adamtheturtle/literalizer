require "set"
module Fixture_zig_record_fallback_set_values_Crystal_record_nested_map_fallback
extend self
alias LiteralizerRecordValue = Bool | Float64 | Int128 | Int32 | Int64 | String | Nil
record Record0, name : String, payload : Hash(String, LiteralizerRecordValue)
my_data = [
    Record0.new("one", Hash(String, LiteralizerRecordValue){"scalar" => 1, "items" => Set{2, 3}}),
    Record0.new("two", Hash(String, LiteralizerRecordValue){"other" => 2}),
]
end
