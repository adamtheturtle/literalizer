import io.circe.Json
object Fixture_signed_constructor_arguments_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromInt(-42),
    Json.fromInt(0),
    Json.fromInt(42),
    Json.fromDoubleOrNull(-1.25),
    Json.fromDoubleOrNull(0.0),
    Json.fromDoubleOrNull(1.25),
)
}
