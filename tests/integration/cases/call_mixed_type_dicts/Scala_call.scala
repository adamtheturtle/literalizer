object Check {
class _MgrType { def Op(operation: Any = null): Any = null }
val mgr = new _MgrType
mgr.Op(operation = Map("type" -> "create", "pr_id" -> "pr_1", "draft" -> true))
mgr.Op(operation = Map("type" -> "create", "pr_id" -> "pr_2"))
}
