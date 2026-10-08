import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_literalize_ref_cpp_record_ownership_Scala_ref {
case class Record1(integer: Int, boolean: Boolean, decimal: Double, `null`: Any)
case class Record3(integer: Int)
case class Record2(child: Record3)
case class Record4(text: String)
case class Record5(day: LocalDate, stamp: ZonedDateTime)
case class Record0(trivial: Record1, nested: Record2, owning: Record4, calendar: Record5)
val trivial = Record1(
    integer = 1,
    boolean = true,
    decimal = 1.5,
    `null` = null,
)
val nested = Record2(
    child = Record3(
        integer = 2,
    ),
)
val owning = Record4(
    text = "owned",
)
val calendar = Record5(
    day = LocalDate.of(2001, 1, 2),
    stamp = ZonedDateTime.of(2001, 1, 2, 3, 4, 5, 0, ZoneId.of("UTC")),
)
val my_data = Record0(
    trivial = trivial,
    nested = nested,
    owning = owning,
    calendar = calendar,
)
}
