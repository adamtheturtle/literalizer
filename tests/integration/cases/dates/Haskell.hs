module Fixture_dates_Haskell where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDate Day | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("date", HDate (fromGregorian 2024 1 15)),
    ("datetime", HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000)))
    ]
main :: IO ()
main = seq my_data (return ())
