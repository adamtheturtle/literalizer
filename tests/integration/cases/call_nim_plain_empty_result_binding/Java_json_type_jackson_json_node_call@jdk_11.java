import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object make_widget(Object arg0) { return null; }
    public static void main() throws Exception {
var my_data = make_widget(new ObjectMapper().readTree("[]"));
    }
}
