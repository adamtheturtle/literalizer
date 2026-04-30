import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_heterogeneous_scalars_in_annotated_sequence_Scala_combined {
var my_data = List(
    true,
    1.5,
    null,
    LocalDate.of(2020, 1, 1),
    ZonedDateTime.of(2020, 1, 1, 0, 0, 0, 0, ZoneId.of("Z")),
    List(),
)
my_data = List(
    true,
    1.5,
    null,
    LocalDate.of(2020, 1, 1),
    ZonedDateTime.of(2020, 1, 1, 0, 0, 0, 0, ZoneId.of("Z")),
    List(),
)
}
