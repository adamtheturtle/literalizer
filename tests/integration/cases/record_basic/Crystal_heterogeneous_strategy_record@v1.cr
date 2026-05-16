module Fixture_record_basic_Crystal_heterogeneous_strategy_record
extend self
record Record0, id : Int32, description : String, is_done : Bool, blocks : Array(Int32)
my_data = Record0.new(
    1,
    "She said \"hello\", then waved",
    false,
    [
        1,
        2,
        3,
    ],
)
end
