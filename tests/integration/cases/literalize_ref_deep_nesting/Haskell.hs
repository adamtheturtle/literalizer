module Fixture_literalize_ref_deep_nesting_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("a", HMap [("b", HMap [("c", HMap [("$ref", HStr "deep")])])])
    ]
main :: IO ()
main = seq my_data (return ())
