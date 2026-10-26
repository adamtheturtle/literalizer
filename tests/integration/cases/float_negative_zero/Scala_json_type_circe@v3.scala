import io.circe.Json
object Fixture_float_negative_zero_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromDoubleOrNull(-0.0),
    Json.fromDoubleOrNull(1.5),
)
}
