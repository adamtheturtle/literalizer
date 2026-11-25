module Fixture_sibling_map_rendered_date_Haskell where
import Data.Time (Day, fromGregorian)
data Val = HStr String | HMap [(String, Val)] | HDate Day
my_data :: Val
my_data = HMap [
    ("a", HMap [("k", HDate (fromGregorian 2020 1 1))]),
    ("b", HMap [("k", HStr "string")])
    ]
main :: IO ()
main = seq my_data (return ())
