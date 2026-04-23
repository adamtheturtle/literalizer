class _MgrType { fun op(operation: Any? = null): Any? = null }
class _AppType { val mgr = _MgrType() }
val app = _AppType()
app.mgr.op(operation = mapOf<String, Any?>("type" to "create", "pr_id" to "pr_1", "draft" to true))
app.mgr.op(operation = mapOf<String, Any?>("type" to "create", "pr_id" to "pr_2"))
