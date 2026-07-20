import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object make_widget(Object... args) { return null; }
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("42");
    }
}
