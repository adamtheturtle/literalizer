{-# LANGUAGE QuasiQuotes #-}
module Fixture_bidi_formatting_string_with_nul_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"v": "a‪\u0000é😀b"} |]
main :: IO ()
main = seq my_data (return ())
