object Fixture_call_cpp_identity_nested_method_Scala_call {
class _ThingType { def go(): Any = null }
class _OuterType { val thing = new _ThingType }
val outer = new _OuterType
outer.thing.go()
}
