object Fixture_call_process_root_Scala_call {
class _ApiType { def fetch(data: Any = null): Any = null }
class _ProcessType { val api = new _ApiType }
val process = new _ProcessType
process.api.fetch(data = Map("data" -> "hello"))
process.api.fetch(data = Map("data" -> 42))
process.api.fetch(data = Map("data" -> true))
}
