module Fixture_positional_empty_lists_without_exemplar_Haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [
        HList []
        ],
    HList [
        HList []
        ]
    ]
main :: IO ()
main = seq my_data (return ())
