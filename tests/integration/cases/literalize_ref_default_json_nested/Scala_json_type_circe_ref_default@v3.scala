import io.circe.Json
object Fixture_literalize_ref_default_json_nested_Scala_json_type_circe_ref_default {
val shared: Json = Json.fromInt(42)
val my_data: Json = Json.obj(
    "refs" -> Json.arr(shared, shared),
    "quoted" -> Json.fromString("#{shared}"),
)
}
