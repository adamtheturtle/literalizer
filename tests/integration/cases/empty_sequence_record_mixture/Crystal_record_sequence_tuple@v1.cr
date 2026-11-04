module Fixture_empty_sequence_record_mixture_Crystal_record_sequence_tuple
extend self
record Record0, x : Int32
my_data = {
    Tuple.new,
    Record0.new(1),
}
end
