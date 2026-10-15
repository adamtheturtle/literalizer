object Fixture_literalize_ref_empty_record_sequence_Scala_ref {
case class Record0(x: Int)
val emptyItems = List()
val populatedItems = List(
    Record0(x = 1),
)
val my_data = List[List[Map[String, Int]]](
    emptyItems,
    populatedItems,
)
}
