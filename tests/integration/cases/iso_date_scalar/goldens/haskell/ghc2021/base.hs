module Fixture_iso_date_scalar_Haskell where
import Data.Time (Day, fromGregorian)
data Val = HDate Day
my_data :: Val
my_data = HDate (fromGregorian 2000 1 1)
main :: IO ()
main = seq my_data (return ())
