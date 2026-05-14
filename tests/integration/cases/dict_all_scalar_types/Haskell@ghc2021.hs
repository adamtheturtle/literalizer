module Fixture_dict_all_scalar_types_Haskell where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HMap [(String, Val)] | HDate Day | HDatetime UTCTime
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("s", HStr "string"),
    ("i", 1),
    ("f", 1.5),
    ("b", HBool True),
    ("n", HNull),
    ("d", HDate (fromGregorian 2024 1 15)),
    ("dt", HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 43200))),
    ("by", HStr "48656c6c6f")
    ]
main :: IO ()
main = seq my_data (return ())
