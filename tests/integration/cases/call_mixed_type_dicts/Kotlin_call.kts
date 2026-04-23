class _MgrType { fun Op(operation: Any? = null): Any? = null }
val mgr = _MgrType()
mgr.Op(operation = mapOf<String, Any?>("type" to "create", "pr_id" to "pr_1", "draft" to true))
mgr.Op(operation = mapOf<String, Any?>("type" to "create", "pr_id" to "pr_2"))
