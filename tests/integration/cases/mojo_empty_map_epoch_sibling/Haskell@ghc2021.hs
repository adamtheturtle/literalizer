module Fixture_mojo_empty_map_epoch_sibling_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HStr String | HList [Val] | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HList [
    HMap [("timestamp", HDatetime (UTCTime (fromGregorian 2020 1 1) (secondsToDiffTime 0)))],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
