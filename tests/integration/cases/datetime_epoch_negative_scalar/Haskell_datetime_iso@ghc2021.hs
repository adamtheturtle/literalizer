module Fixture_datetime_epoch_negative_scalar_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "1969-12-31T23:59:59+00:00"
main :: IO ()
main = seq my_data (return ())
