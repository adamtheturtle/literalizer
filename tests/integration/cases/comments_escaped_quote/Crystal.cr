module Fixture_comments_escaped_quote_Crystal
extend self
my_data = {
    "key" => "value \" # not a comment",  # real
}
end
