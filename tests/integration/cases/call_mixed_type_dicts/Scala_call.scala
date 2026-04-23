object Check {
class _MType { def Op(operation: Any = null): Any = null }
val m = new _MType
m.Op(operation = Map("type" -> "create", "pr_id" -> "pr_1", "draft" -> true))
m.Op(operation = Map("type" -> "create", "pr_id" -> "pr_2"))
}
