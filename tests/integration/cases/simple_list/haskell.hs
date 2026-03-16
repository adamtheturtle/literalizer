{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]
instance IsString Val where
    fromString = HStr
instance Num Val where
    fromInteger = HInt
    (+) = error "not implemented"
    (*) = error "not implemented"
    abs = error "not implemented"
    signum = error "not implemented"
    negate = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (fromRational r)
    (/) = error "not implemented"
x :: Val
x = HList [
    1,
    "hello",
    HBool True,
    HNull
]
