module Fixture_datetime_offset_beyond_java_limit_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2020-06-15T12:00:00+23:59"
main :: IO ()
main = seq my_data (return ())
