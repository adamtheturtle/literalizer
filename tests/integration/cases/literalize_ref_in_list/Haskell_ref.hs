module Fixture_literalize_ref_in_list_Haskell_ref where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
x :: Val
x = 0
y :: Val
y = 0
my_data :: Val
my_data = HList [
    x,
    y
    ]
main :: IO ()
main = seq my_data (return ())
