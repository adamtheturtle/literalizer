{-# LANGUAGE QuasiQuotes #-}
module Fixture_sml_negative_epoch_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["1960-01-01T00:00:00+00:00"] |]
main :: IO ()
main = seq my_data (return ())
