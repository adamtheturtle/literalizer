module Fixture_heterogeneous_scalars_in_annotated_sequence_Haskell where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = HNull | HBool Bool | HFloat Double | HList [Val] | HDate Day | HDatetime UTCTime
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HList [
    HBool True,
    1.5,
    HNull,
    HDate (fromGregorian 2020 1 1),
    HDatetime (UTCTime (fromGregorian 2020 1 1) (secondsToDiffTime 0)),
    HList []
    ]
main :: IO ()
main = seq my_data (return ())
