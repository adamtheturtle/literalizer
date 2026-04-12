module Check where
import Data.Time (Day, fromGregorian)
data Val = HDate Day
my_data :: Val
my_data = HDate (fromGregorian 2024 1 15)
