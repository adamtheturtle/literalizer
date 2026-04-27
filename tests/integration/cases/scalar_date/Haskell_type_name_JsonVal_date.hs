module check where
import Data.Time (Day, fromGregorian)
data JsonVal = HDate Day
my_data :: JsonVal
my_data = HDate (fromGregorian 2024 1 15)
