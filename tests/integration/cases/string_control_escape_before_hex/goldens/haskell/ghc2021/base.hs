module Fixture_string_control_escape_before_hex_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "a\x07\&face"
main :: IO ()
main = seq my_data (return ())
