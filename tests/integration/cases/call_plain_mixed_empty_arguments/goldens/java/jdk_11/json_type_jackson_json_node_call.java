import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object make_widget(Object arg0, Object arg1, Object arg2) { return null; }
    public static void main() throws Exception {
make_widget(new ObjectMapper().readTree("[]"), new ObjectMapper().readTree("[1]"), new ObjectMapper().readTree("[]"));
make_widget(new ObjectMapper().readTree("[\"text\"]"), new ObjectMapper().readTree("[2]"), new ObjectMapper().readTree("[]"));
make_widget(new ObjectMapper().readTree("[]"), new ObjectMapper().readTree("[\"text\"]"), new ObjectMapper().readTree("[]"));
make_widget(new ObjectMapper().readTree("[\"text\"]"), new ObjectMapper().readTree("[2]"), new ObjectMapper().readTree("[3]"));
    }
}
