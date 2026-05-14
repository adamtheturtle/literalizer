module Fixture_scalar_date_Haskell_type_hints_safe where
import Data.Time (Day, fromGregorian)
data Val = HDate Day
my_data :: Val
my_data = HDate (fromGregorian 2024 1 15)
main :: IO ()
main = seq my_data (return ())
