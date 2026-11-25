class Check {
class ThingType_ { public object? go(object? before = null, object? populated = null, object? after = null) => null; }
static ThingType_ thing = new ThingType_();
    public static void Main() {
thing.go(new object?[] {}, new int[] {1}, new object?[] {});
thing.go(new string[] {"text"}, new int[] {2}, new object?[] {});
thing.go(new object?[] {}, new string[] {"text"}, new object?[] {});
thing.go(new string[] {"text"}, new int[] {2}, new int[] {3});
    }
}
