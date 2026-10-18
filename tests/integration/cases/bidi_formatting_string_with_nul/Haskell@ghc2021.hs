module Fixture_bidi_formatting_string_with_nul_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("v", HStr "a\x202a\x00é😀b")
    ]
main :: IO ()
main = seq my_data (return ())
