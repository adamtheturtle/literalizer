module Fixture_literalize_ref_default_nested_Haskell_ref_default where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
item_var :: Val
item_var = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = HMap [
    ("items", HList [item_var, HMap [("fallback", HStr "value")]])
    ]
main :: IO ()
main = seq my_data (return ())
