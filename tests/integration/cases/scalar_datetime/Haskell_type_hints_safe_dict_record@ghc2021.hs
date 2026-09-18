{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_scalar_datetime_Haskell_type_hints_safe_dict_record where
import Data.Time
my_data :: UTCTime
my_data = UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000)
main :: IO ()
main = seq my_data (return ())
