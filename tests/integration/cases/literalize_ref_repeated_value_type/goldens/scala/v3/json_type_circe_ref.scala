import io.circe.Json
object Fixture_literalize_ref_repeated_value_type_Scala_json_type_circe_ref {
val shared: Json = Json.fromInt(42)
val my_data: Json = Json.arr(
    shared,
    shared,
)
}
