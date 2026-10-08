module Fixture_v_four_dimensional_empty_lists_Haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [
        HList [
            HList []
            ]
        ],
    HList [
        HList [
            HList []
            ]
        ]
    ]
main :: IO ()
main = seq my_data (return ())
