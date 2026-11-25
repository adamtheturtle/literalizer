object Fixture_call_plain_mixed_empty_arguments_Scala_call {
def make_widget(before: Any = null, populated: Any = null, after: Any = null): Any = null
make_widget(before = List(), populated = List[Int](1), after = List())
make_widget(before = List[String]("text"), populated = List[Int](2), after = List())
make_widget(before = List(), populated = List[String]("text"), after = List())
make_widget(before = List[String]("text"), populated = List[Int](2), after = List[Int](3))
}
