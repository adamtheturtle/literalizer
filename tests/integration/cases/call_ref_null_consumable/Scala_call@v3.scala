object Fixture_call_ref_null_consumable_Scala_call {
def consume(value: Any = null): Any = null
val my_null = null
val regular_null = null
consume(value = my_null)
consume(value = regular_null)
}
