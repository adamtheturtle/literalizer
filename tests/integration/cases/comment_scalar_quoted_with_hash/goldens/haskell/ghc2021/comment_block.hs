module Fixture_comment_scalar_quoted_with_hash_Haskell_comment_block where
data Val = HStr String
my_data :: Val
my_data = HStr "hello # world"  {- note -}
main :: IO ()
main = seq my_data (return ())
