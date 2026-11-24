module Fixture_comment_block_scalar_not_comment_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("description", HStr "# not a comment\n"),
    ("name", HStr "foo")
    ]
main :: IO ()
main = seq my_data (return ())
