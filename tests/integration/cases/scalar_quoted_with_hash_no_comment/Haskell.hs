module Fixture_scalar_quoted_with_hash_no_comment_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "hello # world"
main :: IO ()
main = seq my_data (return ())
