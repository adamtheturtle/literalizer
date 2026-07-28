object Fixture_call_unknown_ref_nested_Scala_call {
def process(known_value: Any = null, nested_missing: Any = null): Any = null
val known_value = true
val unknown_value = true
process(known_value = known_value, nested_missing = unknown_value)
}
