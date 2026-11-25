module Fixture_comments_trailing_Haskell_comment_block where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a"
    {- trailing -}
    ]
main :: IO ()
main = seq my_data (return ())
