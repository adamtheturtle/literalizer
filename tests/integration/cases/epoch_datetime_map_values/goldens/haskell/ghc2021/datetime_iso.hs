module Fixture_epoch_datetime_map_values_Haskell_datetime_iso where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("within_i32", HStr "2024-01-15T12:00:00"),
    ("beyond_i32", HStr "2099-06-15T08:30:00")
    ]
main :: IO ()
main = seq my_data (return ())
