import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume_widget(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode item = new ObjectMapper().readTree("null");
JsonNode my_data = new ObjectMapper().readTree("null");
consume_widget(my_data);
my_data = new ObjectMapper().readTree("null");
consume_widget(my_data);
    }
}
