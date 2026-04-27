module Fixture_comments_escaped_quote_crystal
extend self
my_data = {
    "key" => "value \" # not a comment",  # real
}
end
