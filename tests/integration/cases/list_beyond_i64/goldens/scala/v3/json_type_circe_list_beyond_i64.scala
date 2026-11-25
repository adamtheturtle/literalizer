import io.circe.Json
object Fixture_list_beyond_i64_Scala_json_type_circe_list_beyond_i64 {
val my_data: Json = Json.arr(
    Json.fromLong(9223372036854775807L),
    Json.fromBigInt(BigInt("9223372036854775808")),
)
}
