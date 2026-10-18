module Fixture_millisecond_datetime_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("half", HDatetime (UTCTime (fromGregorian 1979 5 27) (picosecondsToDiffTime 27120500000000000))),
    ("milli", HDatetime (UTCTime (fromGregorian 1979 5 27) (picosecondsToDiffTime 27120100000000000))),
    ("max_milli", HDatetime (UTCTime (fromGregorian 1979 5 27) (picosecondsToDiffTime 27120999000000000))),
    ("whole", HDatetime (UTCTime (fromGregorian 1979 5 27) (secondsToDiffTime 27120)))
    ]
main :: IO ()
main = seq my_data (return ())
