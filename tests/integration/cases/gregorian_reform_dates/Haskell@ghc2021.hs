module Fixture_gregorian_reform_dates_Haskell where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime, picosecondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDate Day | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("ancient_date", HDate (fromGregorian 1500 3 1)),
    ("modern_date", HDate (fromGregorian 2024 1 15)),
    ("before_date", HDate (fromGregorian 1582 10 4)),
    ("gap_date", HDate (fromGregorian 1582 10 10)),
    ("transition_date", HDate (fromGregorian 1582 10 15)),
    ("after_date", HDate (fromGregorian 1582 10 16)),
    ("before_naive", HDatetime (UTCTime (fromGregorian 1582 10 4) (picosecondsToDiffTime 45000000001000000))),
    ("gap_naive", HDatetime (UTCTime (fromGregorian 1582 10 10) (picosecondsToDiffTime 45000500000000000))),
    ("transition_positive", HDatetime (UTCTime (fromGregorian 1582 10 14) (secondsToDiffTime 23400))),
    ("transition_negative", HDatetime (UTCTime (fromGregorian 1582 10 16) (secondsToDiffTime 63000))),
    ("after_positive", HDatetime (UTCTime (fromGregorian 1582 10 15) (secondsToDiffTime 23400)))
    ]
main :: IO ()
main = seq my_data (return ())
