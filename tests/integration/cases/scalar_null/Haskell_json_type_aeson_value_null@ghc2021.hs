{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_null_Haskell_json_type_aeson_value_null where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| null |]
main :: IO ()
main = seq my_data (return ())
