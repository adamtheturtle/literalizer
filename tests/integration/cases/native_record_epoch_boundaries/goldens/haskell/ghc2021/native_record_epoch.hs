{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_native_record_epoch_boundaries_Haskell_native_record_epoch where
data Val0 = Val0 { before_epoch :: Integer, after_epoch :: Integer }
my_data :: Val0
my_data = Val0 {
    before_epoch = -1,
    after_epoch = 1
}
main :: IO ()
main = seq my_data (return ())
