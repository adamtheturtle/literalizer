module Fixture_epoch_scalar_below_i32_range_Haskell_type_hints_safe where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 1901 12 13) (secondsToDiffTime 74751))
main :: IO ()
main = seq my_data (return ())
