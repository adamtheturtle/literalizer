{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_variable_form_no_args_Haskell_call where
make_widget :: IO Val
make_widget = return undefined
data Val = HList [Val]
my_data = make_widget
main :: IO ()
main = seq my_data (return ())
