module Fixture_early_year_dates_Haskell where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDate Day | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("date", HDate (fromGregorian 99 5 27)),
    ("naive", HDatetime (UTCTime (fromGregorian 1 1 1) (secondsToDiffTime 45000))),
    ("recent", HDatetime (UTCTime (fromGregorian 2024 5 27) (secondsToDiffTime 36000)))
    ]
main :: IO ()
main = seq my_data (return ())
