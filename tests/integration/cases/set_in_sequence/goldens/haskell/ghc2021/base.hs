module Fixture_set_in_sequence_Haskell where
data Val = HStr String | HList [Val] | HSet [Val]
my_data :: Val
my_data = HList [
    HSet [HStr "a", HStr "b"]
    ]
main :: IO ()
main = seq my_data (return ())
