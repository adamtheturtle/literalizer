import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_type_hints_Scala_type_hints_safe {
val my_data = Map(
    "name" -> "Alice",
    "age" -> 30,
    "active" -> true,
    "score" -> null,
    "joined" -> LocalDate.of(2024, 1, 15),
    "last_login" -> ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("+00:00")),
    "avatar" -> "48656c6c6f",
)
}
