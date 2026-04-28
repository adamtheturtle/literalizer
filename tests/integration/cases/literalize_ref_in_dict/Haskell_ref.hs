module Fixture_literalize_ref_in_dict_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("key", myVar)
    ]
main :: IO ()
main = seq my_data (return ())
