import io.circe.Json
object Fixture_sequence_ragged_siblings_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.arr(Json.fromString("set_task"), Json.fromString("web"), Json.fromString("lint_web")),
    Json.arr(Json.fromString("merge_pipelines")),
)
}
