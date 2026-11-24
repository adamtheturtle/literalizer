module Fixture_string_nul_before_hex_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("x", HStr "before\x00\&after")
    ]
main :: IO ()
main = seq my_data (return ())
