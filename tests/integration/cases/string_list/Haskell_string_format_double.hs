{-# LANGUAGE OverloadedStrings #-}
module Fixture_string_list_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "foo",
    "bar",
    "baz"
    ]
