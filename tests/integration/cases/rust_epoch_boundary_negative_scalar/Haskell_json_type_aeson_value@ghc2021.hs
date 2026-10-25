{-# LANGUAGE QuasiQuotes #-}
module Fixture_rust_epoch_boundary_negative_scalar_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "1901-12-13T20:45:51Z" |]
main :: IO ()
main = seq my_data (return ())
