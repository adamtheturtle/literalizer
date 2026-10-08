module Fixture_csharp_fallback_map_non_scalar_Crystal_record_nested_map_fallback_multiline
extend self
alias LiteralizerRecordValue = Bool | Float64 | Int128 | Int32 | Int64 | String | Nil
record Record0, name : String, payload : Hash(String, LiteralizerRecordValue)
my_data = [
    Record0.new(
        "one",
        Hash(String, LiteralizerRecordValue){
            "scalar" => 1,
            "items" => [
                2,
                3,
            ],
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
