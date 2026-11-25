module Fixture_bom_string_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("x", HStr "\xfeff")
    ]
main :: IO ()
main = seq my_data (return ())
