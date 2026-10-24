{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_json_repeated_object_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
consume :: Value -> IO ()
consume _ = return ()
shared :: Value
shared = [aesonQQ| {"value": [1, 2]} |]
main :: IO ()
main = do
    _ <- consume [aesonQQ| {"left": {"$ref": "shared"}, "right": {"$ref": "shared"}} |]
    pure ()
