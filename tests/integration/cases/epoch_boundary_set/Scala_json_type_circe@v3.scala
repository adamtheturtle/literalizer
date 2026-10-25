import io.circe.Json
object Fixture_epoch_boundary_set_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("1901-12-13T20:45:51"),
    Json.fromString("1901-12-13T20:45:52"),
    Json.fromString("2038-01-19T03:14:07"),
    Json.fromString("2038-01-19T03:14:08"),
)
}
