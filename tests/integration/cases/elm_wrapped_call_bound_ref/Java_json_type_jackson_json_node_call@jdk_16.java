import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object make_widget(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode value = new ObjectMapper().readTree("1");
make_widget(value);
    }
}
