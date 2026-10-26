module Fixture_scalar_datetime_seconds_microsecond_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2024-01-15T12:30:45.123456"
main :: IO ()
main = seq my_data (return ())
