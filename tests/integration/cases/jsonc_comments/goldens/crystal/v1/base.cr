module Fixture_jsonc_comments_Crystal
extend self
my_data = {
    # A JSONC input case with both comment forms.
    "url" => "https://example.org/a/*b*/",  # detail
    # continued
    "count" => 2,  # trailing line comment
}
end
