module Fixture_literalize_ref_go_later_record_imports_Crystal_ref
extend self
record Record1, x : Int32
record Record2, day : Time, stamp : String
record Record0, plain : Record1, timed : Record2
plain = Record1.new(
    1,
)
timed = Record2.new(
    Time.utc(2001, 1, 2),
    "2001-01-02T03:04:05+00:00",
)
my_data = Record0.new(
    plain,
    timed,
)
end
