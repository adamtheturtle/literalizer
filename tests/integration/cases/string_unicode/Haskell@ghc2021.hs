module Fixture_string_unicode_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "café",
    HStr "中文"
    ]
main :: IO ()
main = seq my_data (return ())
