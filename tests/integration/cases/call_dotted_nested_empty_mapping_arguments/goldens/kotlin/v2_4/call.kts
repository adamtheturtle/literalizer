class _WorkerType { fun process(values: Any? = null, count: Any? = null): Any? = listOf<Any?>(values, count) }
class _ApiType { val worker = _WorkerType() }
val api = _ApiType()
api.worker.process(values = listOf<Any?>(1, mapOf<String, Any?>()), count = 42)
api.worker.process(values = listOf<Any?>(2, mapOf<String, String>("x" to "s")), count = 43)
