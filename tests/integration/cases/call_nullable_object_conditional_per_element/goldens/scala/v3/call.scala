object Fixture_call_nullable_object_conditional_per_element_Scala_call {
def make_widget(count: Any = null): Any = null
val my_data = if (make_widget(count = 7) != null)
    make_widget(count = 7) // inner
else null // trailing
}
