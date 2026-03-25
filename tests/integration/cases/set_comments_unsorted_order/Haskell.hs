{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HStr String | HSet [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HSet [
    -- before apple
    "apple",
    "banana"  -- banana inline
    -- trailing
    ]
