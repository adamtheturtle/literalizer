module Fixture_json5_comment_like_strings_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "// data",
    HStr "/* data */",
    HStr "escaped quote: \" // data",
    HStr "backslash: \\"
    ]
main :: IO ()
main = seq my_data (return ())
