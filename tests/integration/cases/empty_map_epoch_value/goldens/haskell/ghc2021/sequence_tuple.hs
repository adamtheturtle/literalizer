module Fixture_empty_map_epoch_value_Haskell_sequence_tuple where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HStr String | HList [Val] | HMap [(String, Val)] | HDatetime UTCTime
my_data :: (Val, Val)
my_data = (
    HMap [("timestamp", HDatetime (UTCTime (fromGregorian 2020 1 1) (secondsToDiffTime 0)))],
    HMap []
    )
main :: IO ()
main = seq my_data (return ())
