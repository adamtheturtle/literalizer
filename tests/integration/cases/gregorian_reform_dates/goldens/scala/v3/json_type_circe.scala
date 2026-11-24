import io.circe.Json
object Fixture_gregorian_reform_dates_Scala_json_type_circe {
val my_data: Json = Json.obj(
    "ancient_date" -> Json.fromString("1500-03-01"),
    "modern_date" -> Json.fromString("2024-01-15"),
    "before_date" -> Json.fromString("1582-10-04"),
    "gap_date" -> Json.fromString("1582-10-10"),
    "transition_date" -> Json.fromString("1582-10-15"),
    "after_date" -> Json.fromString("1582-10-16"),
    "before_naive" -> Json.fromString("1582-10-04T12:30:00.000001"),
    "gap_naive" -> Json.fromString("1582-10-10T12:30:00.500000"),
    "transition_positive" -> Json.fromString("1582-10-15T00:30:00+18:00"),
    "transition_negative" -> Json.fromString("1582-10-15T23:30:00-18:00"),
    "after_positive" -> Json.fromString("1582-10-16T00:30:00+18:00"),
)
}
