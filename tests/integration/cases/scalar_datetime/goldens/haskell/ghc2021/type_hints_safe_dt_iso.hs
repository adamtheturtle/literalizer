module Fixture_scalar_datetime_Haskell_type_hints_safe_dt_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2024-01-15T12:30:00+00:00"
main :: IO ()
main = seq my_data (return ())
