module Fixture_jsonc_output_timestamp_input_roundtrip_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    -- event time
    ("when", HStr "2024-01-15T12:34:56+00:00")
    ]
main :: IO ()
main = seq my_data (return ())
