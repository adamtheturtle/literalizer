class _ApiType { fun fetch(data: Any? = null): Any? = listOf<Any?>(data) }
class _ProcessType { val api = _ApiType() }
val process = _ProcessType()
process.api.fetch(data = mapOf<String, Any?>("data" to "hello"))
process.api.fetch(data = mapOf<String, Any?>("data" to 42))
process.api.fetch(data = mapOf<String, Any?>("data" to true))
