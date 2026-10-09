module Fixture_literalize_ref_swift_nullable_records_Crystal_ref
extend self
record Record1, x : Int32, y : Nil
record Record2, x : Nil, y : Nil
record Record3, x : Int32, y : Int32
record Record0, nullable : Record1, null_fields : Record2, plain : Record3
nullable = Record1.new(
    1,
    nil,
)
null_fields = Record2.new(
    nil,
    nil,
)
plain = Record3.new(
    1,
    2,
)
my_data = Record0.new(
    nullable,
    null_fields,
    plain,
)
end
