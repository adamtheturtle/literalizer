module Fixture_json5_raw_line_separators_Crystal
extend self
my_data = {
    "double" => "a b",
    "single" => "c d",
    # A comment, which both separators would end.
    "both" => "e f g",
    "continued" => "hi",
    "escaped backslash" => "j\\ k",
}
end
