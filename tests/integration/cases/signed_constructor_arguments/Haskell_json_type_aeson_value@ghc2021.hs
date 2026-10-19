{-# LANGUAGE QuasiQuotes #-}
module Fixture_signed_constructor_arguments_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [-42, 0, 42, -1.25, 0.0, 1.25] |]
main :: IO ()
main = seq my_data (return ())
