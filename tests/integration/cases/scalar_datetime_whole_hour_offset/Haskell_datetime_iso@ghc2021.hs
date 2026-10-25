module Fixture_scalar_datetime_whole_hour_offset_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2024-01-15T18:00:00+05:00"
main :: IO ()
main = seq my_data (return ())
