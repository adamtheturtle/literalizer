object Fixture_call_nullable_conditional_collection_Scala_call_nested {
def make_widget(count: Any = null): Any = null
val my_data = (
if (make_widget(count = List[Int](1, 2)) != null)
    make_widget(count = List[Int](1, 2)) // inner
else null // trailing
)
}
