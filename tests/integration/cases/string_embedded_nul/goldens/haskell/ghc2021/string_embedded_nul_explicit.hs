module Fixture_string_embedded_nul_Haskell_string_embedded_nul_explicit where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("x", HStr "\x00"),
    ("y", HStr "\x00\&1")
    ]
main :: IO ()
main = seq my_data (return ())
