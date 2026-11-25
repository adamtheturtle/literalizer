import io.circe.Json
object Fixture_literalize_ref_value_type_hint_Scala_json_type_circe_ref {
val refData: Json = Json.arr(
    Json.fromInt(1),
    Json.fromInt(2),
)
val my_data: Json = refData
}
