{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_scalar_date_Haskell_type_hints_safe_dict_record where
import Data.Time
my_data :: Day
my_data = fromGregorian 2024 1 15
main :: IO ()
main = seq my_data (return ())
