import java.time.LocalDate
import java.time.ZoneId
import java.time.ZonedDateTime
object Fixture_literalize_ref_go_later_record_imports_Scala_ref {
case class Record1(x: Int)
case class Record2(day: LocalDate, stamp: ZonedDateTime)
case class Record0(plain: Record1, timed: Record2)
val plain = Record1(
    x = 1,
)
val timed = Record2(
    day = LocalDate.of(2001, 1, 2),
    stamp = ZonedDateTime.of(2001, 1, 2, 3, 4, 5, 0, ZoneId.of("UTC")),
)
val my_data = Record0(
    plain = plain,
    timed = timed,
)
}
