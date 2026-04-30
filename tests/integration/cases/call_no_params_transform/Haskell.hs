module Fixture_call_no_params_transform_Haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [],
    HList []
    ]
main :: IO ()
main = seq my_data (return ())
