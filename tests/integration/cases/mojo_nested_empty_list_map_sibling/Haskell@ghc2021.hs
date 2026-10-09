module Fixture_mojo_nested_empty_list_map_sibling_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("values", HList [])],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
