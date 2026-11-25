import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("call", "send"), Map.entry("args", new Object[]{1, "email", "a@gmail.com", 100})),
    Map.ofEntries(Map.entry("call", "recv"), Map.entry("args", new Object[]{2, "sms", "b@example.com", 200}))
};
    }
}
