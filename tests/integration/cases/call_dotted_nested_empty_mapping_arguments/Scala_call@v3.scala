object Fixture_call_dotted_nested_empty_mapping_arguments_Scala_call {
class _WorkerType { def process(values: Any = null, count: Any = null): Any = null }
class _ApiType { val worker = new _WorkerType }
val api = new _ApiType
api.worker.process(values = List(1, Map()), count = 42)
api.worker.process(values = List(2, Map[String, String]("x" -> "s")), count = 43)
}
