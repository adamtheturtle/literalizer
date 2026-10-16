{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_nim_empty_statement_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
make_widget :: Value -> IO ()
make_widget _ = return ()
main :: IO ()
main = do
    _ <- make_widget [aesonQQ| [] |]
    pure ()
