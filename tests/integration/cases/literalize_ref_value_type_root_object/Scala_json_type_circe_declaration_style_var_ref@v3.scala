import io.circe.Json
object Fixture_literalize_ref_value_type_root_object_Scala_json_type_circe_declaration_style_var_ref {
var shared: Json = Json.obj(
    "field" -> Json.arr(Json.fromInt(1), Json.fromInt(2)),
)
var my_data: Json = shared
}
