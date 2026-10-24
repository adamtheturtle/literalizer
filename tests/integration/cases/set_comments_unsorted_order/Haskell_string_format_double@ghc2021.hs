{-# LANGUAGE OverloadedStrings #-}
module Fixture_set_comments_unsorted_order_Haskell_string_format_double where
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
main :: IO ()
main = seq my_data (return ())
