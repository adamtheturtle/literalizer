module Fixture_v_empty_map_epoch_nested_value_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HStr String | HList [Val] | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HList [
    HMap [("nested", HMap [("times", HList [HDatetime (UTCTime (fromGregorian 1900 1 1) (secondsToDiffTime 0))])])],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
