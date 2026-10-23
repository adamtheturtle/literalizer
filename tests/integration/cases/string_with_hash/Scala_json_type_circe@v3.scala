import io.circe.Json
object Fixture_string_with_hash_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("issue #{42}"),
    Json.fromString("color #red"),
)
}
