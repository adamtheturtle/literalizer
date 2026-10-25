import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume_widget(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode shared = new ObjectMapper().readTree("[1, 2]");
JsonNode my_data = new ObjectMapper().readTree("[0]");
consume_widget(my_data);
my_data = new ObjectMapper().readTree("[1, 2]");
consume_widget(my_data);
    }
}
