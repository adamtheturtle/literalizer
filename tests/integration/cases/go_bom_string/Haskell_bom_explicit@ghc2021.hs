module Fixture_go_bom_string_Haskell_bom_explicit where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("x", HStr "\xfeff")
    ]
main :: IO ()
main = seq my_data (return ())
