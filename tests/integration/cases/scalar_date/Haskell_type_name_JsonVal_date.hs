module Fixture_scalar_date_haskell_type_name_jsonval_date where
import Data.Time (Day, fromGregorian)
data JsonVal = HDate Day
my_data :: JsonVal
my_data = HDate (fromGregorian 2024 1 15)
