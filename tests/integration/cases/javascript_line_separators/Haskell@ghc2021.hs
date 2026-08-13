module Fixture_javascript_line_separators_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a b c",
    HStr "a\r b"
    ]
main :: IO ()
main = seq my_data (return ())
