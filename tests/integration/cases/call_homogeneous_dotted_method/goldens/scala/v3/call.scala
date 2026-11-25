object Fixture_call_homogeneous_dotted_method_Scala_call {
class _ClientType { def fetch(value: Any = null): Any = null }
class _AppType { val client = new _ClientType }
val app = new _AppType
app.client.fetch(value = "hello")
app.client.fetch(value = "world")
}
