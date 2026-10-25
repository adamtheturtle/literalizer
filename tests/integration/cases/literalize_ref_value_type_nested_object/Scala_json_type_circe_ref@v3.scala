import io.circe.Json
object Fixture_literalize_ref_value_type_nested_object_Scala_json_type_circe_ref {
val shared: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val build: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val jsonObject: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val jsonAllocator: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val jsonEntries: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val jsonEntry: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val my_data: Json = Json.obj(
    "field" -> shared,
    "nested" -> Json.arr(shared, Json.obj()),
    "build" -> build,
    "json_object" -> jsonObject,
    "json_allocator" -> jsonAllocator,
    "json_entries" -> jsonEntries,
    "json_entry" -> jsonEntry,
)
}
