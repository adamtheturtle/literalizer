module Fixture_next_line_string_Haskell_type_hints_safe where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("x", HStr "\x85")
    ]
main :: IO ()
main = seq my_data (return ())
