{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_cpp_call_string_result_binding_Haskell_call where
make_widget :: Val -> IO Val
make_widget _ = return undefined
data Val = HStr String
my_data = make_widget (HStr "text")
main :: IO ()
main = seq my_data (return ())
