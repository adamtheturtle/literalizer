import io.circe.Json
object Fixture_bom_string_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "x" -> Json.fromString("﻿"),
)
}
