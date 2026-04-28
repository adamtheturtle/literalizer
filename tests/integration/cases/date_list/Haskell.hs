module Fixture_date_list_Haskell where
import Data.Time (Day, fromGregorian)
data Val = HList [Val] | HDate Day
my_data :: Val
my_data = HList [
    HDate (fromGregorian 2024 1 15),
    HDate (fromGregorian 2024 2 20)
    ]
