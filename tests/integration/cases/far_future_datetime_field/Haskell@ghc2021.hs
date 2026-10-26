module Fixture_far_future_datetime_field_Haskell where
import Data.Time (UTCTime(..), fromGregorian, picosecondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("ts", HDatetime (UTCTime (fromGregorian 3000 12 31) (picosecondsToDiffTime 86399999999000000)))
    ]
main :: IO ()
main = seq my_data (return ())
