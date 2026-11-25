module Fixture_unicode_line_separators_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "a\x85\&b\x2028\&c\x2029\&d\r\x2028\&e"
main :: IO ()
main = seq my_data (return ())
