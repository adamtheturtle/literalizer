object Fixture_call_nullable_object_conditional_existing_Scala_call {
def make_widget(count: Any = null): Any = null
def consume(count: Any = null): Any = null
var my_data = make_widget(count = 7)
consume(count = my_data)
my_data = if (make_widget(count = 13) != null)
    make_widget(count = 13) // inner
else null // trailing
consume(count = my_data)
}
