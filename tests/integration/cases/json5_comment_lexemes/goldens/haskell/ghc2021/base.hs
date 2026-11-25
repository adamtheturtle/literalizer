module Fixture_json5_comment_lexemes_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    -- heading
    ("a", HStr "single ' // data"),
    ("b", HStr "linecontinuation"),
    ("c", HStr "\\"),  -- actual comment
    ("d", HStr "\x2028\x2029")  -- final comment
    ]
main :: IO ()
main = seq my_data (return ())
