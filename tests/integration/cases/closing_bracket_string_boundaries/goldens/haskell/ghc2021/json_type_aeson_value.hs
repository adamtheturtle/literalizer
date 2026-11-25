{-# LANGUAGE QuasiQuotes #-}
module Fixture_closing_bracket_string_boundaries_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["]", "a]", "a]=", "a]b"] |]
main :: IO ()
main = seq my_data (return ())
