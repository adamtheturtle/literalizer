module Fixture_type_hints_Haskell_type_hints_safe where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HStr String | HMap [(String, Val)] | HDate Day | HDatetime UTCTime
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
    ("name", HStr "Alice"),
    ("age", 30),
    ("active", HBool True),
    ("score", HNull),
    ("joined", HDate (fromGregorian 2024 1 15)),
    ("last_login", HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000))),
    ("avatar", HStr "48656c6c6f")
    ]
main :: IO ()
main = seq my_data (return ())
