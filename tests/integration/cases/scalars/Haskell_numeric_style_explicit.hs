{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    HInt 42,
    HFloat (3.14),
    HBool True,
    HBool False,
    "hello \"world\""
    ]
