module Fixture_dollar_ref_is_data_Crystal
extend self
my_data = {
    "value" => {"$ref" => "foo"},
}
end
