module Fixture_nested_record_sequences_Crystal_record_sequence_tuple
extend self
record Record0, a : Int32
my_data = {
     {Record0.new(1)},
     {Record0.new(2)},
}
end
