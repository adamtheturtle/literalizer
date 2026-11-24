module Fixture_early_year_dates_Haskell_prefix_J where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = JStr String | JMap [(String, Val)] | JDate Day | JDatetime UTCTime
my_data :: Val
my_data = JMap [
    ("date", JDate (fromGregorian 99 5 27)),
    ("naive", JDatetime (UTCTime (fromGregorian 1 1 1) (secondsToDiffTime 45000))),
    ("recent", JDatetime (UTCTime (fromGregorian 2024 5 27) (secondsToDiffTime 36000)))
    ]
main :: IO ()
main = seq my_data (return ())
