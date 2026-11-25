module Fixture_comments_sequence_inline_Haskell_comment_block where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a",  {- note a -}
    HStr "b"  {- note b -}
    ]
main :: IO ()
main = seq my_data (return ())
