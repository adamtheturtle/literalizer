import io.circe.Json
object Fixture_literalize_ref_value_type_nested_object_indented_Scala_json_type_circe_ref {
        val shared: Json = Json.arr(
            Json.fromInt(1),
            Json.fromInt(2),
        )
        val my_data: Json = Json.obj(
            "field" -> Json.obj("nested" -> shared),
            "text" -> Json.fromString("first\n{ \" // }"),
        )
}
