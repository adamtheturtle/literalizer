module Fixture_scalar_datetime_haskell_prefix_j_datetime where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = JDatetime UTCTime
my_data :: Val
my_data = JDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000))
