object Fixture_record_basic_Scala_heterogeneous_strategy_record {
case class Record0(id: Int, description: String, is_done: Boolean, blocks: List[Int])
val my_data = Record0(
    id = 1,
    description = "She said \"hello\", then waved",
    is_done = false,
    blocks = List[Int](
        1,
        2,
        3,
    ),
)
}
