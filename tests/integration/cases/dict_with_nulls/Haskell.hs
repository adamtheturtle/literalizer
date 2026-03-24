{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime, picosecondsToDiffTime)
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("name", "Alice"),
    ("score", HNull),
    ("age", 30)
    ]
