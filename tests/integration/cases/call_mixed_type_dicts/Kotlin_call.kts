class _MType { fun Op(operation: Any? = null): Any? = null }
val m = _MType()
m.Op(operation = mapOf<String, Any?>("type" to "create", "pr_id" to "pr_1", "draft" to true))
m.Op(operation = mapOf<String, Any?>("type" to "create", "pr_id" to "pr_2"))
