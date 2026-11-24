module Fixture_epoch_boundary_set_Haskell_datetime_iso where
data Val = HSet [Val] | HStr String
my_data :: Val
my_data = HSet [
    HStr "1901-12-13T20:45:51",
    HStr "1901-12-13T20:45:52",
    HStr "2038-01-19T03:14:07",
    HStr "2038-01-19T03:14:08"
    ]
main :: IO ()
main = seq my_data (return ())
