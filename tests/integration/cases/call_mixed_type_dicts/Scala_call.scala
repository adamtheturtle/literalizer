object Fixture_call_mixed_type_dicts_Scala_call {
class _MgrType { def op(operation: Any = null): Any = null }
class _AppType { val mgr = new _MgrType }
val app = new _AppType
app.mgr.op(operation = Map("type" -> "create", "pr_id" -> "pr_1", "draft" -> true))
app.mgr.op(operation = Map("type" -> "create", "pr_id" -> "pr_2"))
}
