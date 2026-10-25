module Fixture_rust_epoch_boundary_scalar_Haskell_type_hints_safe where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2099 6 15) (secondsToDiffTime 30600))
main :: IO ()
main = seq my_data (return ())
