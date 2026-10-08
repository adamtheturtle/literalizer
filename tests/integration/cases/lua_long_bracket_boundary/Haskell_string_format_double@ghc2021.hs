{-# LANGUAGE OverloadedStrings #-}
module Fixture_lua_long_bracket_boundary_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "]",
    "a]",
    "a]=",
    "a]b"
    ]
main :: IO ()
main = seq my_data (return ())
