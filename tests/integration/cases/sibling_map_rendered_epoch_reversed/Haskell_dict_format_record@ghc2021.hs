{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_sibling_map_rendered_epoch_reversed_Haskell_dict_format_record where
import Data.Time
data Val1 = Val1 { k :: Integer }
data Val2 = Val2 { k :: UTCTime }
data Val0 = Val0 { b :: Val1, a :: Val2 }
my_data :: Val0
my_data = Val0 {
    b = Val1 {
        k = 1
    },
    a = Val2 {
        k = UTCTime (fromGregorian 2040 1 1) (secondsToDiffTime 0)
    }
}
main :: IO ()
main = seq my_data (return ())
