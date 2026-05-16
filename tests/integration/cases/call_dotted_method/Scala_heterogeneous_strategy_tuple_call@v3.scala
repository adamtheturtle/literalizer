object Fixture_call_dotted_method_Scala_heterogeneous_strategy_tuple_call {
class _ClientType { def fetch(payload: Any = null): Any = null }
class _AppType { val client = new _ClientType }
val app = new _AppType
app.client.fetch(payload = "hello")
app.client.fetch(payload = 42)
app.client.fetch(payload = true)
}
