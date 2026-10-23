module Fixture_datetime_list_Haskell_sequence_tuple where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HList [Val] | HDatetime UTCTime
my_data :: (Val, Val)
my_data = (
    HDatetime (UTCTime (fromGregorian 2024 1 15) (picosecondsToDiffTime 45000123456000000)),
    HDatetime (UTCTime (fromGregorian 2024 6 1) (secondsToDiffTime 28800))
    )
main :: IO ()
main = seq my_data (return ())
