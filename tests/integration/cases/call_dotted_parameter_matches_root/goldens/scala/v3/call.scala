object Fixture_call_dotted_parameter_matches_root_Scala_call {
class _OuterType { def inner(outer: Any = null, n: Any = null): Any = null }
val outer = new _OuterType
outer.inner(outer = 1, n = 2)
}
