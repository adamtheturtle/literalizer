module Fixture_empty_ref_key_Haskell_ref_default where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
external_value :: Val
external_value = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = HList [
    external_value
    ]
main :: IO ()
main = seq my_data (return ())
