import io.circe.Json
object Fixture_float_special_values_Scala_json_type_circe_float_specials {
val my_data: Json = Json.arr(
    Json.fromDoubleOrNull(Double.PositiveInfinity),
    Json.fromDoubleOrNull(Double.NegativeInfinity),
    Json.fromDoubleOrNull(Double.NaN),
)
}
