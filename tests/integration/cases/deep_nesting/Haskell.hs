import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
{-# LANGUAGE OverloadedStrings #-}
module Check where
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
    ("level1", HMap [("level2", HMap [("level3", HMap [("level4", HMap [("value", "deep"), ("items", HList ["a", "b"])])]), ("sibling", 42)]), ("tags", HList [HMap [("name", "tag1"), ("meta", HMap [("priority", 1), ("labels", HList ["x", "y"])])]])])
    ]
