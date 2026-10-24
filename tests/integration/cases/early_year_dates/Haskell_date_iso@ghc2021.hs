module Fixture_early_year_dates_Haskell_date_iso where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("date", HStr "0099-05-27"),
    ("naive", HDatetime (UTCTime (fromGregorian 1 1 1) (secondsToDiffTime 45000))),
    ("recent", HDatetime (UTCTime (fromGregorian 2024 5 27) (secondsToDiffTime 36000)))
    ]
main :: IO ()
main = seq my_data (return ())
