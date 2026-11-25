object Fixture_call_dotted_receiver_parameter_collisions_Scala_call {
class _WorkerType { def process(self: Any = null, self_ : Any = null): Any = null }
class _ApiType { val worker = new _WorkerType }
val api = new _ApiType
api.worker.process(self = Map(), self_ = Map())
}
