module Fixture_literalize_ref_record_alias_never_Crystal_ref
extend self
record Record0, x : Int32, y : Nil
value = Record0.new(
    1,
    nil,
)
my_data = value
end
