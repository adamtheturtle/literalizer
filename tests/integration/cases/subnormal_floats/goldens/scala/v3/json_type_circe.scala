import io.circe.Json
object Fixture_subnormal_floats_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromDoubleOrNull(5.0e-324),
    Json.fromDoubleOrNull(-5.0e-324),
    Json.fromDoubleOrNull(1.0e-310),
)
}
