import io.circe.Json
object Fixture_literalize_ref_value_type_nested_object_Scala_json_type_circe_declaration_style_var_ref {
var shared: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
var build: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
var jsonObject: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
var jsonAllocator: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
var jsonEntries: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
var jsonEntry: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
var my_data: Json = Json.obj(
    "field" -> shared,
    "nested" -> Json.arr(shared, Json.obj()),
    "build" -> build,
    "json_object" -> jsonObject,
    "json_allocator" -> jsonAllocator,
    "json_entries" -> jsonEntries,
    "json_entry" -> jsonEntry,
)
}
