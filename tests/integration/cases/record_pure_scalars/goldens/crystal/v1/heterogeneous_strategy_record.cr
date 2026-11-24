module Fixture_record_pure_scalars_Crystal_heterogeneous_strategy_record
extend self
record Record0, name : String, age : Int32, active : Bool, score : Float64
my_data = Record0.new(
    "Alice",
    30,
    true,
    4.5,
)
end
