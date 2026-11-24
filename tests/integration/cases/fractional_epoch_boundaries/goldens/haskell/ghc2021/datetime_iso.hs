module Fixture_fractional_epoch_boundaries_Haskell_datetime_iso where
data Val = HList [Val] | HStr String
my_data :: Val
my_data = HList [
    HStr "1970-01-01T00:00:00.000001+00:00",
    HStr "1969-12-31T23:59:59.500000+00:00",
    HStr "1970-01-01T00:00:01+00:00"
    ]
main :: IO ()
main = seq my_data (return ())
