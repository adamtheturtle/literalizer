object Fixture_record_nested_container_Scala_heterogeneous_strategy_record {
case class Record0(title: String, tags: List[String], priority: Int)
val my_data = Record0(
    title = "report",
    tags = List[String](
        "draft",
        "urgent",
        "review",
    ),
    priority = 2,
)
}
