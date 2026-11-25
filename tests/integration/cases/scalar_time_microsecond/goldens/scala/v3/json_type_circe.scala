import io.circe.Json
object Fixture_scalar_time_microsecond_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "exact_millisecond" -> Json.fromString("09:30:15.123000"),
    "sub_millisecond" -> Json.fromString("09:30:15.123456"),
)
}
