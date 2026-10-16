{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_nim_plain_empty_result_binding_Haskell_call where
make_widget :: Val -> IO Val
make_widget _ = return undefined
data Val = HList [Val]
my_data = make_widget (HList [])
main :: IO ()
main = seq my_data (return ())
