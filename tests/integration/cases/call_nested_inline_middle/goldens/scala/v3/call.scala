object Fixture_call_nested_inline_middle_Scala_call {
def f(ops: Any = null): Any = null
f(ops = List[List[String]](List[String]("DEL", "b", "10"), List[String]("ADD", "a", "x")))  // note
// next call
f(ops = List[List[String]](List[String]("ADD", "c", "y")))
}
