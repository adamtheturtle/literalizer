module Fixture_record_sequence_mixture_controls_Crystal_record_sequence_tuple
extend self
record Record0, x : Int32
my_data = {
     { {1}, Record0.new(1)},
     {Record0.new(1), Record0.new(2)},
     {Tuple.new,  {Record0.new(1)}},
     {Tuple.new, Tuple.new},
}
end
