module Fixture_comments_empty_line_Haskell_comment_block where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a",
    {- -}
    HStr "b"
    ]
main :: IO ()
main = seq my_data (return ())
