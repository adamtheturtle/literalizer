object Fixture_native_record_list_Scala_record_sequence_array {
case class Record1(age: Int)
case class Record0(name: String, active: Boolean, count: Int, score: Double, missing: Any, scores: Array[Int], child: Record1)
val my_data = Array(
    Record0(name = "Ada", active = true, count = 1, score = 1.5, missing = null, scores = Array[Int](1, 2), child = Record1(age = 3)),
    Record0(name = "Bob", active = false, count = 2, score = 2.5, missing = null, scores = Array[Int](4), child = Record1(age = 5)),
)
}
