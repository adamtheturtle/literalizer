module Fixture_jsonc_comment_strings_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    -- strings stay data
    HStr "https://example.org/a/*b*/",  -- URL annotation
    HStr "escaped quote: \" // still data",
    HStr "backslash: \\",  -- outside the string
    HStr "/* not a comment */"
    ]
main :: IO ()
main = seq my_data (return ())
