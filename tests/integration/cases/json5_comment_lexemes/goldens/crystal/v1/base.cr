module Fixture_json5_comment_lexemes_Crystal
extend self
my_data = {
    # heading
    "a" => "single ' // data",
    "b" => "linecontinuation",
    "c" => "\\",  # actual comment
    "d" => "  ",  # final comment
}
end
