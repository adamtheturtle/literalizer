class _WorkerType { fun process(self: Any? = null, self_: Any? = null): Any? = listOf<Any?>(self, self_) }
class _ApiType { val worker = _WorkerType() }
val api = _ApiType()
api.worker.process(self = mapOf<String, Any?>(), self_ = mapOf<String, Any?>())
