module Fixture_native_record_special_float_fields_Crystal_record_sequence_tuple
extend self
record Record0, positive : Float64, negative : Float64, nan_value : Float64, finite : Float64
my_data = Record0.new(
    Float64::INFINITY,
    -Float64::INFINITY,
    Float64::NAN,
    1.5,
)
end
