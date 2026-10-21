using System;
class Check {
class ThingType_ { public object? go(object? before = null, object? populated = null, object? after = null) => null; }
static ThingType_ thing = new ThingType_();
    public static void Main() {
thing.go(ValueTuple.Create(), ValueTuple.Create(1), ValueTuple.Create());
thing.go(ValueTuple.Create("text"), ValueTuple.Create(2), ValueTuple.Create());
thing.go(ValueTuple.Create(), ValueTuple.Create("text"), ValueTuple.Create());
thing.go(ValueTuple.Create("text"), ValueTuple.Create(2), ValueTuple.Create(3));
    }
}
