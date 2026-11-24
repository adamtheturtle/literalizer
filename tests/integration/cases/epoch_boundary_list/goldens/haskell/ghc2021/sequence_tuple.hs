module Fixture_epoch_boundary_list_Haskell_sequence_tuple where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HList [Val] | HDatetime UTCTime
my_data :: (Val, Val, Val, Val)
my_data = (
    HDatetime (UTCTime (fromGregorian 1901 12 13) (secondsToDiffTime 74751)),
    HDatetime (UTCTime (fromGregorian 1901 12 13) (secondsToDiffTime 74752)),
    HDatetime (UTCTime (fromGregorian 2038 1 19) (secondsToDiffTime 11647)),
    HDatetime (UTCTime (fromGregorian 2038 1 19) (secondsToDiffTime 11648))
    )
main :: IO ()
main = seq my_data (return ())
