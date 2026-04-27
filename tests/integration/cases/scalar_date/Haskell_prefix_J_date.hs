module Fixture_scalar_date_haskell_prefix_j_date where
import Data.Time (Day, fromGregorian)
data Val = JDate Day
my_data :: Val
my_data = JDate (fromGregorian 2024 1 15)
