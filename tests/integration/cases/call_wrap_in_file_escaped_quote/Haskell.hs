module Fixture_call_wrap_in_file_escaped_quote_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HList [HStr "a\"b"]
    ]
main :: IO ()
main = seq my_data (return ())
