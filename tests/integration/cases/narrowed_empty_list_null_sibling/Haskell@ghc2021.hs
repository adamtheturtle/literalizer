module Fixture_narrowed_empty_list_null_sibling_Haskell where
data Val = HNull | HList [Val]
my_data :: Val
my_data = HList [
    HList [HNull],
    HList []
    ]
main :: IO ()
main = seq my_data (return ())
