module Fixture_tuple_record_field_Crystal_heterogeneous_strategy_record
extend self
record Record0, call : String, args : Array(Int32 | String)
my_data = Record0.new(
    "send",
    [
        1,
        "email",
        "a@gmail.com",
        100,
    ],
)
end
