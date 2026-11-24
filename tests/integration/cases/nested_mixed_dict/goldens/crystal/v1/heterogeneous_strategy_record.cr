module Fixture_nested_mixed_dict_Crystal_heterogeneous_strategy_record
extend self
record Record1, a : Int32, b : String, c : Nil
record Record0, outer : Record1
my_data = Record0.new(
    Record1.new(
        1,
        "x",
        nil,
    ),
)
end
