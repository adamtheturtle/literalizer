module Fixture_rust_epoch_boundary_scalar_Haskell_datetime_iso where
data Val = HStr String
my_data :: Val
my_data = HStr "2099-06-15T08:30:00"
main :: IO ()
main = seq my_data (return ())
