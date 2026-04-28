module Fixture_scalar_date_Haskell_type_name_JsonVal_date where
import Data.Time (Day, fromGregorian)
data JsonVal = HDate Day
my_data :: JsonVal
my_data = HDate (fromGregorian 2024 1 15)
main :: IO ()
main = seq my_data (return ())
