module Fixture_unicode_line_separators_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "ab c d"
main :: IO ()
main = seq my_data (return ())
