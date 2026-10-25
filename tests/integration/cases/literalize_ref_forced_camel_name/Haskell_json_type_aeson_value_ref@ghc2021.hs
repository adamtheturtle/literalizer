{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_forced_camel_name_Haskell_json_type_aeson_value_ref where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
userObj :: Value
userObj = [aesonQQ| {"_": "_"} |]
my_data :: Value
my_data = [aesonQQ| {"$ref": "USER_OBJ"} |]
main :: IO ()
main = seq my_data (return ())
