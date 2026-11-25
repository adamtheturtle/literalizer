class _ProcessType { fun fetch(data: Any? = null): Any? = listOf<Any?>(data) }
class _AppType { val process = _ProcessType() }
val app = _AppType()
app.process.fetch(data = mapOf<String, Any?>("data" to "hello"))
app.process.fetch(data = mapOf<String, Any?>("data" to 42))
app.process.fetch(data = mapOf<String, Any?>("data" to true))
