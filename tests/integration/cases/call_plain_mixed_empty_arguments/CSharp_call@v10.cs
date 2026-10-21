using System;
class Check {
static object? make_widget(object? before = null, object? populated = null, object? after = null) => null;
    public static void Main() {
make_widget(ValueTuple.Create(), ValueTuple.Create(1), ValueTuple.Create());
make_widget(ValueTuple.Create("text"), ValueTuple.Create(2), ValueTuple.Create());
make_widget(ValueTuple.Create(), ValueTuple.Create("text"), ValueTuple.Create());
make_widget(ValueTuple.Create("text"), ValueTuple.Create(2), ValueTuple.Create(3));
    }
}
