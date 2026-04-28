module Fixture_comments_double_hash_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    -- # section
    HStr "a"
    ]
main :: IO ()
main = seq my_data (return ())
