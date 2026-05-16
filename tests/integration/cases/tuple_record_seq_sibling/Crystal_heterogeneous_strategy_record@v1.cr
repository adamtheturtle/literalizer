module Fixture_tuple_record_seq_sibling_Crystal_heterogeneous_strategy_record
extend self
record Record0, scores : Array(Int32), args : Array(Int32 | String)
my_data = Record0.new(
    [
        10,
        20,
        30,
    ],
    [
        1,
        "email",
        "a@gmail.com",
        100,
    ],
)
end
