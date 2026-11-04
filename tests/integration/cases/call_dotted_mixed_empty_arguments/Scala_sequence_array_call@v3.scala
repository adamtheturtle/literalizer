object Fixture_call_dotted_mixed_empty_arguments_Scala_sequence_array_call {
class _ThingType { def go(before: Any = null, populated: Any = null, after: Any = null): Any = null }
val thing = new _ThingType
thing.go(before = Array.empty[Any], populated = Array[Int](1), after = Array.empty[Any])
thing.go(before = Array[String]("text"), populated = Array[Int](2), after = Array.empty[Any])
thing.go(before = Array.empty[Any], populated = Array[String]("text"), after = Array.empty[Any])
thing.go(before = Array[String]("text"), populated = Array[Int](2), after = Array[Int](3))
}
