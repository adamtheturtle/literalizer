object Fixture_call_composed_record_headers_without_hints_Scala_heterogeneous_strategy_record_call {
case class Record0(name: String, values: List[Int])
def consume(value: Any = null): Any = null
val item = Record0(
    name = "first",
    values = List[Int](
        1,
        2,
    ),
)
consume(value = item)
}
