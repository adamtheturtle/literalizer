module Fixture_typed_sibling_maps_empty_values_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("m", HMap [])],
    HMap [("m", HMap [])]
    ]
main :: IO ()
main = seq my_data (return ())
