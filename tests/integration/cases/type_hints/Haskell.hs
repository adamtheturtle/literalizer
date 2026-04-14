module Check where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HStr String | HMap [(String, Val)] | HDate Day | HDatetime UTCTime
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
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
