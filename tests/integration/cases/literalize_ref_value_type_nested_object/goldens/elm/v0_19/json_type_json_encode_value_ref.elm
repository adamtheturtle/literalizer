module Check exposing (..)


import Json.Encode


shared : Json.Encode.Value
shared = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
build : Json.Encode.Value
build = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
jsonObject : Json.Encode.Value
jsonObject = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
jsonAllocator : Json.Encode.Value
jsonAllocator = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
jsonEntries : Json.Encode.Value
jsonEntries = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
jsonEntry : Json.Encode.Value
jsonEntry = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("field", shared),
    ("nested", Json.Encode.list identity [shared, Json.Encode.object []]),
    ("build", build),
    ("json_object", jsonObject),
    ("json_allocator", jsonAllocator),
    ("json_entries", jsonEntries),
    ("json_entry", jsonEntry)
    ]
