module Fixture_literalize_ref_deep_nesting_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
deep :: Val
deep = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = HMap [
    ("a", HMap [("b", HMap [("c", deep)])])
    ]
main :: IO ()
main = seq my_data (return ())
