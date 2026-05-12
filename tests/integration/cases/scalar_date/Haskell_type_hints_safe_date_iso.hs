module Fixture_scalar_date_Haskell_type_hints_safe_date_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2024-01-15"
main :: IO ()
main = seq my_data (return ())
