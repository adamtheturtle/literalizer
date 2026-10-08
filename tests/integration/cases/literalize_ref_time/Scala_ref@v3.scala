import java.time.LocalTime
object Fixture_literalize_ref_time_Scala_ref {
val myTime = LocalTime.of(1, 2, 3)
val my_data = Map[String, LocalTime](
    "x" -> myTime,
)
}
