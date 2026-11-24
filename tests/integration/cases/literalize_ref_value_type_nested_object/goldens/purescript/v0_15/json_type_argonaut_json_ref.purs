module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


shared :: Json
shared = fromRight jsonNull (jsonParser "[1, 2]")
build :: Json
build = fromRight jsonNull (jsonParser "[1, 2]")
jsonObject :: Json
jsonObject = fromRight jsonNull (jsonParser "[1, 2]")
jsonAllocator :: Json
jsonAllocator = fromRight jsonNull (jsonParser "[1, 2]")
jsonEntries :: Json
jsonEntries = fromRight jsonNull (jsonParser "[1, 2]")
jsonEntry :: Json
jsonEntry = fromRight jsonNull (jsonParser "[1, 2]")
my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"field\": {\"$ref\": \"shared\"}, \"nested\": [{\"$ref\": \"shared\"}, {}], \"build\": {\"$ref\": \"build\"}, \"json_object\": {\"$ref\": \"json_object\"}, \"json_allocator\": {\"$ref\": \"json_allocator\"}, \"json_entries\": {\"$ref\": \"json_entries\"}, \"json_entry\": {\"$ref\": \"json_entry\"}}")
