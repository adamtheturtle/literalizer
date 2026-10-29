module Fixture_literalize_ref_repeated_record_Crystal_ref
extend self
record Record0, value : Array(Int32)
shared = Record0.new(
    [
        1,
        2,
    ],
)
my_data = [
    shared,
    shared,
]
end
