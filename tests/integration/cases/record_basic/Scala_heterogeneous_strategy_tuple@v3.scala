object Fixture_record_basic_Scala_heterogeneous_strategy_tuple {
case class Record0(id: Int, label: String, enabled: Boolean, related_ids: List[Int])
val my_data = Record0(
    id = 1,
    label = "She said \"hello\", then waved",
    enabled = false,
    related_ids = List[Int](
        1,
        2,
        3,
    ),
)
}
