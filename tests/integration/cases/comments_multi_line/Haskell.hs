module Fixture_comments_multi_line_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    -- line 1
    -- line 2
    HStr "a"
    ]
main :: IO ()
main = seq my_data (return ())
