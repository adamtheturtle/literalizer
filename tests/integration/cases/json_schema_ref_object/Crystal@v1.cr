module Fixture_json_schema_ref_object_Crystal
extend self
my_data = {
    "schema" => {"$ref" => "#/defs/Foo"},
}
end
