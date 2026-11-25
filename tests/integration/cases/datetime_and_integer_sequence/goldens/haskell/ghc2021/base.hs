module Fixture_datetime_and_integer_sequence_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HInt Integer | HList [Val] | HDatetime UTCTime
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HList [
    HDatetime (UTCTime (fromGregorian 2000 1 1) (secondsToDiffTime 3723)),
    1
    ]
main :: IO ()
main = seq my_data (return ())
