module Fixture_yaml_encoding_cookie_comment_Haskell where
data Val = HStr String
-- coding: ascii
my_data :: Val
my_data = HStr "café"
main :: IO ()
main = seq my_data (return ())
