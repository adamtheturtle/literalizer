module Fixture_record_fallback_map_non_scalar_Crystal_record_sequence_tuple
extend self
alias LiteralizerRecordValue = Bool | Float64 | Int128 | Int32 | Int64 | String | Tuple(Int32, Int32) | Nil
record Record0, name : String, payload : Hash(String, LiteralizerRecordValue)
my_data = {
    Record0.new("one", Hash(String, LiteralizerRecordValue){"scalar" => 1, "items" => {2, 3}}),
    Record0.new("two", Hash(String, LiteralizerRecordValue){"other" => 2}),
}
end
