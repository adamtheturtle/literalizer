object Fixture_call_carrier_nested_separate_Scala_heterogeneous_strategy_record_call {
class _ClientType { def go(first_value: Any = null, second_value: Any = null): Any = null }
class _AppType { val client = new _ClientType }
val app = new _AppType
app.client.go(first_value = List[Int](1), second_value = List[String]("text"))
}
