{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_with_dollar_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["price $10", "$HOME"] |]
main :: IO ()
main = seq my_data (return ())
