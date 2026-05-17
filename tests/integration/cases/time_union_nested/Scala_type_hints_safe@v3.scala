import java.time.LocalTime
object Fixture_time_union_nested_Scala_type_hints_safe {
val my_data = Map[String, List[List[LocalTime]]](
    "mixed" -> List[List[LocalTime]](List[LocalTime](LocalTime.of(9, 30)), List[LocalTime]()),
)
}
