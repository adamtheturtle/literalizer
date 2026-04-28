module Fixture_scalar_date_Haskell_prefix_J_date where
import Data.Time (Day, fromGregorian)
data Val = JDate Day
my_data :: Val
my_data = JDate (fromGregorian 2024 1 15)
