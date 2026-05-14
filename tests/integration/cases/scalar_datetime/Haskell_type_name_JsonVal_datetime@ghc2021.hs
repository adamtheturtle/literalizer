module Fixture_scalar_datetime_Haskell_type_name_JsonVal_datetime where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data JsonVal = HDatetime UTCTime
my_data :: JsonVal
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000))
main :: IO ()
main = seq my_data (return ())
