module Fixture_comment_scalar_before_and_inline_Haskell_comment_block where
data Val = HStr String
{- before -}
my_data :: Val
my_data = HStr "plain"  {- inline -}
main :: IO ()
main = seq my_data (return ())
