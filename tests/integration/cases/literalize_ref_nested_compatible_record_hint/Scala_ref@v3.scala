object Fixture_literalize_ref_nested_compatible_record_hint_Scala_ref {
case class Record1(items: List[Int])
case class Record0(outer: Record1)
val recordData = Record1(
    items = List[Int](
        1,
        2,
    ),
)
val my_data = Record0(
    outer = recordData,
)
}
