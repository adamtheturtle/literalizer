{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_gregorian_reform_dates_Haskell_dict_format_record where
import Data.Time
data Val0 = Val0 { ancient_date :: Day, modern_date :: Day, before_date :: Day, gap_date :: Day, transition_date :: Day, after_date :: Day, before_naive :: UTCTime, gap_naive :: UTCTime, transition_positive :: UTCTime, transition_negative :: UTCTime, after_positive :: UTCTime }
my_data :: Val0
my_data = Val0 {
    ancient_date = fromGregorian 1500 3 1,
    modern_date = fromGregorian 2024 1 15,
    before_date = fromGregorian 1582 10 4,
    gap_date = fromGregorian 1582 10 10,
    transition_date = fromGregorian 1582 10 15,
    after_date = fromGregorian 1582 10 16,
    before_naive = UTCTime (fromGregorian 1582 10 4) (picosecondsToDiffTime 45000000001000000),
    gap_naive = UTCTime (fromGregorian 1582 10 10) (picosecondsToDiffTime 45000500000000000),
    transition_positive = UTCTime (fromGregorian 1582 10 14) (secondsToDiffTime 23400),
    transition_negative = UTCTime (fromGregorian 1582 10 16) (secondsToDiffTime 63000),
    after_positive = UTCTime (fromGregorian 1582 10 15) (secondsToDiffTime 23400)
}
main :: IO ()
main = seq my_data (return ())
