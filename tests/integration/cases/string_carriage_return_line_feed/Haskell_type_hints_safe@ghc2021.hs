module Fixture_string_carriage_return_line_feed_Haskell_type_hints_safe where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("cr", HStr "a\rb"),
    ("crlf", HStr "a\r\nb"),
    ("lf", HStr "a\nb")
    ]
main :: IO ()
main = seq my_data (return ())
