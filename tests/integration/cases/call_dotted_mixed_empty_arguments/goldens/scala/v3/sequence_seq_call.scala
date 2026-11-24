object Fixture_call_dotted_mixed_empty_arguments_Scala_sequence_seq_call {
class _ThingType { def go(before: Any = null, populated: Any = null, after: Any = null): Any = null }
val thing = new _ThingType
thing.go(before = Seq(), populated = Seq(1), after = Seq())
thing.go(before = Seq("text"), populated = Seq(2), after = Seq())
thing.go(before = Seq(), populated = Seq("text"), after = Seq())
thing.go(before = Seq("text"), populated = Seq(2), after = Seq(3))
}
