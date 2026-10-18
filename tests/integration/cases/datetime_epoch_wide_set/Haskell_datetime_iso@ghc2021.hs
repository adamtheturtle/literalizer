module Fixture_datetime_epoch_wide_set_Haskell_datetime_iso where
data Val = HSet [Val] | HStr String
my_data :: Val
my_data = HSet [
    HStr "2099-06-15T08:30:00"
    ]
main :: IO ()
main = seq my_data (return ())
