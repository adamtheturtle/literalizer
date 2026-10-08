module Fixture_literalize_ref_cpp_record_ownership_Crystal_ref
extend self
record Record1, integer : Int32, boolean : Bool, decimal : Float64, null : Nil
record Record3, integer : Int32
record Record2, child : Record3
record Record4, text : String
record Record5, day : Time, stamp : String
record Record0, trivial : Record1, nested : Record2, owning : Record4, calendar : Record5
trivial = Record1.new(
    1,
    true,
    1.5,
    nil,
)
nested = Record2.new(
    Record3.new(
        2,
    ),
)
owning = Record4.new(
    "owned",
)
calendar = Record5.new(
    Time.utc(2001, 1, 2),
    "2001-01-02T03:04:05+00:00",
)
my_data = Record0.new(
    trivial,
    nested,
    owning,
    calendar,
)
end
