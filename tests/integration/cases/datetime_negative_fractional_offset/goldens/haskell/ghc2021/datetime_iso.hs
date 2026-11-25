module Fixture_datetime_negative_fractional_offset_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2000-01-01T00:00:00-05:30"
main :: IO ()
main = seq my_data (return ())
