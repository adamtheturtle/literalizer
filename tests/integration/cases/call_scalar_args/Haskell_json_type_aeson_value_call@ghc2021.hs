{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_scalar_args_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
process :: Value -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- process [aesonQQ| "hello" |]
    _ <- process [aesonQQ| 42 |]
    _ <- process [aesonQQ| true |]
    pure ()
