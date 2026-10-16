object Fixture_call_nim_dotted_mixed_empty_arguments_Scala_call {
class _ThingType { def go(before: Any = null, populated: Any = null, after: Any = null): Any = null }
val thing = new _ThingType
thing.go(before = List(), populated = List[Int](1), after = List())
thing.go(before = List[String]("text"), populated = List[Int](2), after = List())
thing.go(before = List(), populated = List[String]("text"), after = List())
thing.go(before = List[String]("text"), populated = List[Int](2), after = List[Int](3))
}
