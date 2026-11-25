{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_datetime_epoch_wide_carrier_Haskell_dict_format_record where
import Data.Time
data Val0 = Val0 { within_i32 :: UTCTime, beyond_i32 :: UTCTime }
my_data :: Val0
my_data = Val0 {
    within_i32 = UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 43200),
    beyond_i32 = UTCTime (fromGregorian 2099 6 15) (secondsToDiffTime 30600)
}
main :: IO ()
main = seq my_data (return ())
