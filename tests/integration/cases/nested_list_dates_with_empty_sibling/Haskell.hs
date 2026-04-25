module Check where
import Data.Time (Day, fromGregorian)
data Val = HList [Val] | HDate Day
my_data :: Val
my_data = HList [
    HList [HDate (fromGregorian 2026 1 1), HDate (fromGregorian 2026 1 2)],
    HList [],
    HList [HDate (fromGregorian 2026 2 3), HDate (fromGregorian 2026 2 4)]
    ]
