import io.circe.Json
object Fixture_map_beyond_i64_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "a" -> Json.fromLong(9223372036854775807L),
    "b" -> Json.fromBigInt(BigInt("9223372036854775808")),
)
}
