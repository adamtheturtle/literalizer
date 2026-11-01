module Fixture_native_datetime_offsets_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HStr String | HList [Val] | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("stamps", HList [HDatetime (UTCTime (fromGregorian 2001 2 3) (secondsToDiffTime 14705)), HDatetime (UTCTime (fromGregorian 2001 2 3) (secondsToDiffTime 14707)), HDatetime (UTCTime (fromGregorian 2001 2 3) (picosecondsToDiffTime 14705999999000000)), HDatetime (UTCTime (fromGregorian 2001 2 3) (picosecondsToDiffTime 14706000001000000)), HDatetime (UTCTime (fromGregorian 2001 2 2) (picosecondsToDiffTime 81290999999000000)), HDatetime (UTCTime (fromGregorian 2001 2 3) (picosecondsToDiffTime 34521000001000000))])
    ]
main :: IO ()
main = seq my_data (return ())
