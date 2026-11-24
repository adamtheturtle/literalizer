module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "[\"C:\\\\path\\\\to\\\\file\", \"back\\\\\\\\slash\", \"hello \\\\\\\"world\\\\\\\"\", \"path\\\\to \\\"# file\", \"trailing\\\\\", \"both \\\"quotes''' here\", \"line1\\\\nline2\\nwith newline\"]")
