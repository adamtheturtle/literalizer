require "set"
module Fixture_record_fallback_empty_and_mixed_set_values_Crystal_record_nested_map_fallback_multiline
extend self
alias LiteralizerRecordValue = Bool | Float64 | Int128 | Int32 | Int64 | Set(Int32 | String) | Set(String) | String | Nil
record Record0, name : String, payload : Hash(String, LiteralizerRecordValue)
my_data = [
    Record0.new(
        "one",
        Hash(String, LiteralizerRecordValue){
            "scalar" => 1,
            "empty" => Set(String).new,
            "mixed" => Set{
                2,
                "word",
            },
        },
    ),
    Record0.new(
        "two",
        Hash(String, LiteralizerRecordValue){
            "other" => 2,
        },
    ),
]
end
