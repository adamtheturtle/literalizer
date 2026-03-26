{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HBool Bool | HStr String | HList [Val] | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    HMap [("type", "create"), ("pr_id", "pr_1"), ("draft", HBool True)],
    HMap [("type", "create"), ("pr_id", "pr_2")]
    ]
