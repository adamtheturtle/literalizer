module Fixture_scalar_datetime_naive_Haskell_datetime_haskell_naive where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000))
