module Fixture_binary_Haskell_bytes_format_base64 where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "SGVsbG8="
    ]
main :: IO ()
main = seq my_data (return ())
