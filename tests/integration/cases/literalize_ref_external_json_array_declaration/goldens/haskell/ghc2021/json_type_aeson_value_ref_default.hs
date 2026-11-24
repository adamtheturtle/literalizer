{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_external_json_array_declaration_Haskell_json_type_aeson_value_ref_default where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
consume_widget :: Value -> IO ()
consume_widget _ = return ()
shared :: Value
shared = [aesonQQ| [1, 2] |]
my_data :: Value
my_data = shared
main :: IO ()
main = do
    _ <- consume_widget my_data
    pure ()
