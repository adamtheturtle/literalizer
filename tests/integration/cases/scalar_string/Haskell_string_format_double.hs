{-# LANGUAGE OverloadedStrings #-}
module check where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "hello"
