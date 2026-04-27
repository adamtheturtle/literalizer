module Fixture_string_escaped_quotes_and_dashes_haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "hello \"world\" -- not a comment"
