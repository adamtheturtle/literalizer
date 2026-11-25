object Fixture_literalize_ref_repeated_record_Scala_ref {
case class Record0(value: List[Int])
val shared = Record0(
    value = List[Int](
        1,
        2,
    ),
)
val my_data = List(
    shared,
    shared,
)
}
