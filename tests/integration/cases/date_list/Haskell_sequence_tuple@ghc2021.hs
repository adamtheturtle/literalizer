module Fixture_date_list_Haskell_sequence_tuple where
import Data.Time (Day, fromGregorian)
data Val = HList [Val] | HDate Day
my_data :: (Val, Val)
my_data = (
    HDate (fromGregorian 2024 1 15),
    HDate (fromGregorian 2024 2 20)
    )
main :: IO ()
main = seq my_data (return ())
