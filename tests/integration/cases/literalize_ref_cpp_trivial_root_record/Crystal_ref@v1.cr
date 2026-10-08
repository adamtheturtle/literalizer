module Fixture_literalize_ref_cpp_trivial_root_record_Crystal_ref
extend self
record Record1, value : Int32
record Record0, child : Record1
first = Record0.new(
    Record1.new(
        1,
    ),
)
my_data = first
end
