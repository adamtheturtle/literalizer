module Fixture_literalize_ref_single_line_record_declarations_Crystal_ref
extend self
record Record1, x : String
record Record2, x : Int32
record Record0, direct : Record1, bound : Record2
first = Record2.new(
    1,
)
my_data = Record0.new(
    Record1.new(
        "s",
    ),
    first,
)
end
