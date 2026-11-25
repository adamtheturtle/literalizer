module Fixture_string_raw_json_terminator_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    (")json", HStr "x")
    ]
main :: IO ()
main = seq my_data (return ())
