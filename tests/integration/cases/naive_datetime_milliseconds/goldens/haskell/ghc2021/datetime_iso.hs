module Fixture_naive_datetime_milliseconds_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2024-01-15T12:30:01.123000"
main :: IO ()
main = seq my_data (return ())
