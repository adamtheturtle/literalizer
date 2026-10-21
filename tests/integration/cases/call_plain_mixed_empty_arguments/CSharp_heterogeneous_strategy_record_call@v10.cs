class Check {
static object? make_widget(object? before = null, object? populated = null, object? after = null) => null;
    public static void Main() {
make_widget(new object?[] {}, new int[] {1}, new object?[] {});
make_widget(new string[] {"text"}, new int[] {2}, new object?[] {});
make_widget(new object?[] {}, new string[] {"text"}, new object?[] {});
make_widget(new string[] {"text"}, new int[] {2}, new int[] {3});
    }
}
