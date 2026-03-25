module Check where
import Data.Time (Day, fromGregorian)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day
my_data :: Val
my_data = HSet [
    HDate (fromGregorian 2024 1 15),
    HDate (fromGregorian 2024 6 1)
]
