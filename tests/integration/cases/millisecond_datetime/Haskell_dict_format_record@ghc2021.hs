{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_millisecond_datetime_Haskell_dict_format_record where
import Data.Time
data Val0 = Val0 { half :: UTCTime, milli :: UTCTime, max_milli :: UTCTime, whole :: UTCTime }
my_data :: Val0
my_data = Val0 {
    half = UTCTime (fromGregorian 1979 5 27) (picosecondsToDiffTime 27120500000000000),
    milli = UTCTime (fromGregorian 1979 5 27) (picosecondsToDiffTime 27120100000000000),
    max_milli = UTCTime (fromGregorian 1979 5 27) (picosecondsToDiffTime 27120999000000000),
    whole = UTCTime (fromGregorian 1979 5 27) (secondsToDiffTime 27120)
}
main :: IO ()
main = seq my_data (return ())
