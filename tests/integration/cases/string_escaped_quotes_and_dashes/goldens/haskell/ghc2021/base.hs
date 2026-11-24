module Fixture_string_escaped_quotes_and_dashes_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "hello \"world\" -- not a comment"
main :: IO ()
main = seq my_data (return ())
