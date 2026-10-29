module Fixture_negative_epoch_datetime_list_Haskell_datetime_iso where
data Val = HList [Val] | HStr String
my_data :: Val
my_data = HList [
    HStr "1960-01-01T00:00:00+00:00"
    ]
main :: IO ()
main = seq my_data (return ())
