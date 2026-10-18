module Fixture_empty_map_nested_epoch_value_Haskell_datetime_iso where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("nested", HMap [("times", HList [HStr "1900-01-01T00:00:00+00:00"])])],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
