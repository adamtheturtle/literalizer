{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_toml_dotted_key_comments_Haskell_dict_format_record where
data Val1 = Val1 { b :: Integer, c :: Integer }
data Val0 = Val0 { a :: Val1 }
my_data :: Val0
my_data = Val0 {
    a = Val1 {
        b = 1,
        c = 2
    }
}
main :: IO ()
main = seq my_data (return ())
