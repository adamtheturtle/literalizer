{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_json_repeated_scalar_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
consume :: Value -> IO ()
consume _ = return ()
shared :: Value
shared = [aesonQQ| 42 |]
main :: IO ()
main = do
    _ <- consume [aesonQQ| [#{shared}, #{shared}] |]
    pure ()
