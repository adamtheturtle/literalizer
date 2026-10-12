module Fixture_v_empty_map_nested_value_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HList [HMap [("mapping", HMap [])], HMap []],
    HList [HMap [], HMap [("mapping", HMap [])]]
    ]
main :: IO ()
main = seq my_data (return ())
