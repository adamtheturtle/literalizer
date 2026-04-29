module Fixture_literalize_ref_in_list_Haskell_ref where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
valX :: Val
valX = HMap [
    ("_", HStr "_")
    ]
valY :: Val
valY = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = HList [
    valX,
    valY
    ]
main :: IO ()
main = seq my_data (return ())
