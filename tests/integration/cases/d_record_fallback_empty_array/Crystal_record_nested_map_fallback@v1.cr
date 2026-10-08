module Fixture_d_record_fallback_empty_array_Crystal_record_nested_map_fallback
extend self
alias LiteralizerRecordValue = Array(Nil) | Bool | Float64 | Int128 | Int32 | Int64 | String | Nil
record Record0, name : String, payload : Hash(String, LiteralizerRecordValue)
my_data = [
    Record0.new("one", Hash(String, LiteralizerRecordValue){"scalar" => 1, "items" => [] of Nil}),
    Record0.new("two", Hash(String, LiteralizerRecordValue){"other" => 2}),
]
end
