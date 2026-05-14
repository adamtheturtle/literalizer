module Fixture_times_heterogeneous_with_dates_Haskell where
import Data.Time (Day, fromGregorian)
data Val = HStr String | HList [Val] | HMap [(String, Val)] | HDate Day
my_data :: Val
my_data = HMap [
    ("vals", HList [HDate (fromGregorian 2024 1 15), HStr "09:30:00"])
    ]
main :: IO ()
main = seq my_data (return ())
