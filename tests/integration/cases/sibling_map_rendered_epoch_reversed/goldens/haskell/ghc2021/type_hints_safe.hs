module Fixture_sibling_map_rendered_epoch_reversed_Haskell_type_hints_safe where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HInt Integer | HStr String | HMap [(String, Val)] | HDatetime UTCTime
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("b", HMap [("k", 1)]),
    ("a", HMap [("k", HDatetime (UTCTime (fromGregorian 2040 1 1) (secondsToDiffTime 0)))])
    ]
main :: IO ()
main = seq my_data (return ())
