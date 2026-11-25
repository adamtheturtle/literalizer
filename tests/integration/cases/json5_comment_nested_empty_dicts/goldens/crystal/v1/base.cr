module Fixture_json5_comment_nested_empty_dicts_Crystal
extend self
my_data = {
    # outer heading
    # first empty
    "a" => {} of String => String,
    # second empty
    "b" => {} of String => String,
}
end
