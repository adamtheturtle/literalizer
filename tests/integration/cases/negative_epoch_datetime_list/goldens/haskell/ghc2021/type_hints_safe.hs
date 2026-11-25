module Fixture_negative_epoch_datetime_list_Haskell_type_hints_safe where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HList [Val] | HDatetime UTCTime
my_data :: Val
my_data = HList [
    HDatetime (UTCTime (fromGregorian 1960 1 1) (secondsToDiffTime 0))
    ]
main :: IO ()
main = seq my_data (return ())
