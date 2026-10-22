{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_call_purescript_native_record_no_params_Haskell_native_record_call where
consume :: IO ()
consume = return ()
main :: IO ()
main = do
    _ <- consume
    pure ()
