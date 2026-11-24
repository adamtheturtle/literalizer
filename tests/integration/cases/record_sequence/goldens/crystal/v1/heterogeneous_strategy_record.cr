module Fixture_record_sequence_Crystal_heterogeneous_strategy_record
extend self
record Record0, id : Int32, label : String, tags : Array(Nil)
my_data = [
    Record0.new(1, "first", [] of Nil),
    Record0.new(2, "second", [] of Nil),
    Record0.new(3, "third", [] of Nil),
]
end
