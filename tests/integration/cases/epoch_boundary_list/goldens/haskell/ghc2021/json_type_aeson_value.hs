{-# LANGUAGE QuasiQuotes #-}
module Fixture_epoch_boundary_list_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["1901-12-13T20:45:51Z", "1901-12-13T20:45:52Z", "2038-01-19T03:14:07Z", "2038-01-19T03:14:08Z"] |]
main :: IO ()
main = seq my_data (return ())
