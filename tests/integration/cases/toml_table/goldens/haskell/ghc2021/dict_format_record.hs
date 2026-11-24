{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_toml_table_Haskell_dict_format_record where
data Val1 = Val1 { value :: Integer }
data Val0 = Val0 { section :: Val1 }
my_data :: Val0
my_data = Val0 {
    section = Val1 {
        value = 1
    }
}
main :: IO ()
main = seq my_data (return ())
