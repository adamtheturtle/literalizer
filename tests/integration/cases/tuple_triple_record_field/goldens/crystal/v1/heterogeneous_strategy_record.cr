module Fixture_tuple_triple_record_field_Crystal_heterogeneous_strategy_record
extend self
record Record0, call : String, args : Array(Bool | Int32 | String)
my_data = Record0.new(
    "send",
    [
        1,
        "email",
        true,
    ],
)
end
