module Fixture_comments_multi_line_Haskell_comment_block where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    {- line 1 -}
    {- line 2 -}
    HStr "a"
    ]
main :: IO ()
main = seq my_data (return ())
