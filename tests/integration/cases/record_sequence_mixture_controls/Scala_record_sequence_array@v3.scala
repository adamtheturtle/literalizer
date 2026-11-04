object Fixture_record_sequence_mixture_controls_Scala_record_sequence_array {
case class Record0(x: Int)
val my_data = Array[Any](
    Array(Array[Int](1), Record0(x = 1)),
    Array(Record0(x = 1), Record0(x = 2)),
    Array[Any](Array.empty[Any], Array(Record0(x = 1))),
    Array[Any](Array.empty[Any], Array.empty[Any]),
)
}
