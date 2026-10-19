module Fixture_utf8_string_sibling_lines_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "中中中中中中中中中中中中中中中中中中中中",
    HStr "é'é'é'é'é'é'é'é'é'é'",
    HStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
    ]
main :: IO ()
main = seq my_data (return ())
