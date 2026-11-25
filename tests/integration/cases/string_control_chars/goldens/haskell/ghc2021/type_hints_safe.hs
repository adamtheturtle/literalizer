module Fixture_string_control_chars_Haskell_type_hints_safe where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "line1\r\nline2",
    HStr "line1\rline2",
    HStr "\x01"
    ]
main :: IO ()
main = seq my_data (return ())
