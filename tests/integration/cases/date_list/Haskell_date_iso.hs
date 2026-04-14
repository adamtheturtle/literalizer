{-# LANGUAGE OverloadedStrings #-}
module Check where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    "2024-01-15",
    "2024-02-20"
    ]
