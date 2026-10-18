module Fixture_v_sibling_map_rendered_datetime_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("a", HMap [("k", HDatetime (UTCTime (fromGregorian 2020 1 1) (secondsToDiffTime 0)))]),
    ("b", HMap [("k", HStr "string")])
    ]
main :: IO ()
main = seq my_data (return ())
