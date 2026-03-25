module Check where
import Data.Time (Day, fromGregorian)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day
my_data :: Val
my_data = HDate (fromGregorian 2024 1 15)
