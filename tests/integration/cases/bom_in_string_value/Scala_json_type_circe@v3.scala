import io.circe.Json
object Fixture_bom_in_string_value_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "v" -> Json.fromString("a﻿b"),
)
}
