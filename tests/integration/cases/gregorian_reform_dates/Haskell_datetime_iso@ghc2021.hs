module Fixture_gregorian_reform_dates_Haskell_datetime_iso where
import Data.Time (Day, fromGregorian)
data Val = HStr String | HMap [(String, Val)] | HDate Day
my_data :: Val
my_data = HMap [
    ("ancient_date", HDate (fromGregorian 1500 3 1)),
    ("modern_date", HDate (fromGregorian 2024 1 15)),
    ("before_date", HDate (fromGregorian 1582 10 4)),
    ("gap_date", HDate (fromGregorian 1582 10 10)),
    ("transition_date", HDate (fromGregorian 1582 10 15)),
    ("after_date", HDate (fromGregorian 1582 10 16)),
    ("before_naive", HStr "1582-10-04T12:30:00.000001"),
    ("gap_naive", HStr "1582-10-10T12:30:00.500000"),
    ("transition_positive", HStr "1582-10-15T00:30:00+18:00"),
    ("transition_negative", HStr "1582-10-15T23:30:00-18:00"),
    ("after_positive", HStr "1582-10-16T00:30:00+18:00")
    ]
main :: IO ()
main = seq my_data (return ())
