module Fixture_literalize_ref_in_list_Haskell_ref where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    x,
    y
    ]
main :: IO ()
main = seq my_data (return ())
