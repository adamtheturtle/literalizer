module Fixture_empty_key_is_data_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("", HStr "external_value")]
    ]
main :: IO ()
main = seq my_data (return ())
