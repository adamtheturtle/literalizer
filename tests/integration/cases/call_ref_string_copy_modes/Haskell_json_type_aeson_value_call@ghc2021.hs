{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_ref_string_copy_modes_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
consume :: Value -> IO ()
consume _ = return ()
item :: Value
item = [aesonQQ| "s" |]
main :: IO ()
main = do
    _ <- consume item
    pure ()
