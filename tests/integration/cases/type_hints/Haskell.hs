{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
instance IsString Val where
    fromString = HStr
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("name", "Alice"),
    ("age", 30),
    ("active", HBool True),
    ("score", HNull),
    ("joined", HDate (fromGregorian 2024 1 15)),
    ("last_login", HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000))),
    ("avatar", "48656c6c6f")
    ]
