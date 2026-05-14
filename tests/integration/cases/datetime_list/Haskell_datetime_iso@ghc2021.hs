module Fixture_datetime_list_Haskell_datetime_iso where
data Val = HList [Val] | HStr String
my_data :: Val
my_data = HList [
    HStr "2024-01-15T12:30:00.123456+00:00",
    HStr "2024-06-01T08:00:00+00:00"
    ]
main :: IO ()
main = seq my_data (return ())
