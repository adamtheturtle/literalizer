{-# LANGUAGE QuasiQuotes #-}
module Fixture_rust_epoch_boundary_scalar_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "2099-06-15T08:30:00Z" |]
main :: IO ()
main = seq my_data (return ())
