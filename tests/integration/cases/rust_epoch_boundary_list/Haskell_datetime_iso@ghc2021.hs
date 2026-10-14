module Fixture_rust_epoch_boundary_list_Haskell_datetime_iso where
data Val = HList [Val] | HStr String
my_data :: Val
my_data = HList [
    HStr "1901-12-13T20:45:51",
    HStr "1901-12-13T20:45:52",
    HStr "2038-01-19T03:14:07",
    HStr "2038-01-19T03:14:08"
    ]
main :: IO ()
main = seq my_data (return ())
