{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_toml_nested_comments_Haskell_dict_format_record where
data Val1 = Val1 { first :: Integer, second :: Integer }
data Val2 = Val2 { name :: String }
data Val3 = Val3 { inner :: Integer }
data Val0 = Val0 { dotted :: Val1, plain :: Integer, entries :: [Val2], table :: Val3 }
my_data :: Val0
my_data = Val0 {
    dotted = Val1 {
        first = 1,
        second = 2
    },
    plain = 3,
    entries = [
        Val2 {
            name = "one"
        },
        Val2 {
            name = "two"
        }
        ],
    table = Val3 {
        inner = 4
    }
}
main :: IO ()
main = seq my_data (return ())
