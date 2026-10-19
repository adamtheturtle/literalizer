module Fixture_widened_record_map_null_values_Crystal_record_nested_map_fallback
extend self
alias LiteralizerRecordValue = Bool | Float64 | Int128 | Int32 | Int64 | String | Nil
record Record0, input : Hash(String, LiteralizerRecordValue)
my_data = [
    Record0.new(Hash(String, LiteralizerRecordValue){"a" => nil}),
    Record0.new(Hash(String, LiteralizerRecordValue){"b" => nil}),
]
end
