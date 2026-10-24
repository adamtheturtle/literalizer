module Fixture_sml_negative_epoch_Haskell_sequence_tuple where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HList [Val] | HDatetime UTCTime
my_data :: (Val)
my_data = (
    HDatetime (UTCTime (fromGregorian 1960 1 1) (secondsToDiffTime 0))
    )
main :: IO ()
main = seq my_data (return ())
