module Fixture_empty_ordered_map_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap []
main :: IO ()
main = seq my_data (return ())
