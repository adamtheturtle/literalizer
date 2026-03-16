{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]
instance IsString Val where
    fromString = HStr
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate a = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    a / b = error "not implemented"
x :: Val
x = HSet [
    "apple",
    "banana",
    "cherry"
]
