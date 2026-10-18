module Fixture_rust_epoch_boundary_negative_scalar_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "1901-12-13T20:45:51"
main :: IO ()
main = seq my_data (return ())
