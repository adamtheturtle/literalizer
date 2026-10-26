module Fixture_toml_dotted_key_comments_Crystal
extend self
my_data = {
    # first dotted key
    # second dotted key
    "a" => {"b" => 1, "c" => 2},
}
end
