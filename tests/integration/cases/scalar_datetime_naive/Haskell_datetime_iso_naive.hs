module Fixture_scalar_datetime_naive_Haskell_datetime_iso_naive where
data Val = HStr String
my_data :: Val
my_data = HStr "2024-01-15T12:30:00"
main :: IO ()
main = seq my_data (return ())
