object Fixture_call_plain_mixed_empty_arguments_Scala_sequence_seq_call {
def make_widget(before: Any = null, populated: Any = null, after: Any = null): Any = null
make_widget(before = Seq(), populated = Seq(1), after = Seq())
make_widget(before = Seq("text"), populated = Seq(2), after = Seq())
make_widget(before = Seq(), populated = Seq("text"), after = Seq())
make_widget(before = Seq("text"), populated = Seq(2), after = Seq(3))
}
