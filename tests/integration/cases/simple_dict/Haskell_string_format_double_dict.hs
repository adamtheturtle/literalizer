{-# LANGUAGE OverloadedStrings #-}
module Fixture_simple_dict_Haskell_string_format_double_dict where
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("name", "Alice"),
    ("age", 30),
    ("active", HBool True),
    ("score", HNull)
    ]
main :: IO ()
main = seq my_data (return ())
