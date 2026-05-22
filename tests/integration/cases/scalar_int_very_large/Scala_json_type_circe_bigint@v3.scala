import io.circe.Json
object Fixture_scalar_int_very_large_Scala_json_type_circe_bigint {
val my_data: Json = Json.fromBigInt(BigInt("9223372036854775808"))
}
