{-# LANGUAGE OverloadedStrings #-}
module Fixture_dict_keys_and_string_escapes_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
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
    ("plain", HList [1, 2]),
    ("with-dash", "a\nb")
    ]
main :: IO ()
main = seq my_data (return ())
