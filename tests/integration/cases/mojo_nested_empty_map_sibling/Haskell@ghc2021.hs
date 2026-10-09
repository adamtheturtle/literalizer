module Fixture_mojo_nested_empty_map_sibling_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("mapping", HMap [])],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
