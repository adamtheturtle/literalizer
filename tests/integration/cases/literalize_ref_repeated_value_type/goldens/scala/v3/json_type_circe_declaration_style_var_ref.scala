import io.circe.Json
object Fixture_literalize_ref_repeated_value_type_Scala_json_type_circe_declaration_style_var_ref {
var shared: Json = Json.fromInt(42)
var my_data: Json = Json.arr(
    shared,
    shared,
)
}
