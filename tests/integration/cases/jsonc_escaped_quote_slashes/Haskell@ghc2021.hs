module Fixture_jsonc_escaped_quote_slashes_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("text", HStr "a\"//b")
    ]
main :: IO ()
main = seq my_data (return ())
