module Fixture_mojo_empty_map_epoch_sibling_Haskell_datetime_iso where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("timestamp", HStr "2020-01-01T00:00:00+00:00")],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
