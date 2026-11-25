module Fixture_early_year_dates_Haskell_datetime_iso where
import Data.Time (Day, fromGregorian)
data Val = HStr String | HMap [(String, Val)] | HDate Day
my_data :: Val
my_data = HMap [
    ("date", HDate (fromGregorian 99 5 27)),
    ("naive", HStr "0001-01-01T12:30:00"),
    ("recent", HStr "2024-05-27T10:00:00")
    ]
main :: IO ()
main = seq my_data (return ())
