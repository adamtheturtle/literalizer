module Fixture_literalize_ref_crystal_tuple_records_Crystal_ref
extend self
record Record0, field : Int32
value = Record0.new(
    2,
)
my_data = {
    Record0.new(1),
    value,
}
end
