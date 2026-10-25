import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume_widget(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"a\": 0}");
consume_widget(my_data);
my_data = new ObjectMapper().readTree("{\"a\": 1}");
consume_widget(my_data);
    }
}
