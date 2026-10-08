module Fixture_literalize_ref_v_record_empty_map_Crystal_ref
extend self
record Record0, bound : Hash(String, String)
empty_map = {} of String => String
my_data = Record0.new(
    empty_map,
)
end
