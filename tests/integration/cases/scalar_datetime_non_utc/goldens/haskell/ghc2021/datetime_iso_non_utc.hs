module Fixture_scalar_datetime_non_utc_Haskell_datetime_iso_non_utc where
data Val = HStr String
my_data :: Val
my_data = HStr "2024-01-15T18:00:00+05:30"
main :: IO ()
main = seq my_data (return ())
