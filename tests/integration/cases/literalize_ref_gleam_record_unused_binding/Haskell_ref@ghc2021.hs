{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_literalize_ref_gleam_record_unused_binding_Haskell_ref where
data Val0 = Val0 { x :: Integer }
my_data :: Val0
my_data = Val0 {
    x = 1
}
main :: IO ()
main = seq my_data (return ())
