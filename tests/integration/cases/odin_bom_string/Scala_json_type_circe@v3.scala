import io.circe.Json
object Fixture_odin_bom_string_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "v" -> Json.fromString("a﻿b"),
)
}
