module Fixture_string_unicode_Haskell_type_hints_safe where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "café",
    HStr "中文",
    HStr "😀"
    ]
main :: IO ()
main = seq my_data (return ())
