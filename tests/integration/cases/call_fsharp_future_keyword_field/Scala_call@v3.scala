object Fixture_call_fsharp_future_keyword_field_Scala_call {
class _ProcessType { def fetch(data: Any = null): Any = null }
class _AppType { val process = new _ProcessType }
val app = new _AppType
app.process.fetch(data = Map("data" -> "hello"))
app.process.fetch(data = Map("data" -> 42))
app.process.fetch(data = Map("data" -> true))
}
