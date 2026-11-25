import io.circe.Json
object Fixture_noncharacter_string_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "fffe" -> Json.fromString("￾"),
    "ffff" -> Json.fromString("￿"),
)
}
