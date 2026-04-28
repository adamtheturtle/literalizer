module Fixture_date_set_Haskell where
import Data.Time (Day, fromGregorian)
data Val = HSet [Val] | HDate Day
my_data :: Val
my_data = HSet [
    HDate (fromGregorian 2024 1 15),
    HDate (fromGregorian 2024 6 1)
    ]
main :: IO ()
main = seq my_data (return ())
