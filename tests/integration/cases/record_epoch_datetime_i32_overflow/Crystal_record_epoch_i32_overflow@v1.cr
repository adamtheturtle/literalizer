module Fixture_record_epoch_datetime_i32_overflow_Crystal_record_epoch_i32_overflow
extend self
record Record0, within_i32 : Int32, beyond_i32 : Int64
my_data = Record0.new(
    1705320000,
    4085195400,
)
end
