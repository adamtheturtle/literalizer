import io.circe.Json
object Fixture_negative_zero_constructor_arguments_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromDoubleOrNull(-0.0),
    Json.fromDoubleOrNull(0.0),
)
}
