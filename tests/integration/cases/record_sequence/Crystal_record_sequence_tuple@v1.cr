module Fixture_record_sequence_Crystal_record_sequence_tuple
extend self
record Record0, id : Int32, label : String, tags : Tuple()
my_data = {
    Record0.new(1, "first", Tuple.new),
    Record0.new(2, "second", Tuple.new),
    Record0.new(3, "third", Tuple.new),
}
end
