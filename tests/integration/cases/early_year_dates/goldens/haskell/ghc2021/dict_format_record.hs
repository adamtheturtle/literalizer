{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_early_year_dates_Haskell_dict_format_record where
import Data.Time
data Val0 = Val0 { date :: Day, naive :: UTCTime, recent :: UTCTime }
my_data :: Val0
my_data = Val0 {
    date = fromGregorian 99 5 27,
    naive = UTCTime (fromGregorian 1 1 1) (secondsToDiffTime 45000),
    recent = UTCTime (fromGregorian 2024 5 27) (secondsToDiffTime 36000)
}
main :: IO ()
main = seq my_data (return ())
