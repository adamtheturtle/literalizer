module Fixture_empty_orderedmap_with_sibling_Haskell where
data Val = HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [],
    HList []
    ]
main :: IO ()
main = seq my_data (return ())
