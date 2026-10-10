import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object process(Object... args) { return null; }
    public static void main() throws Exception {
process(new ObjectMapper().readTree("\"hello\""));
process(new ObjectMapper().readTree("42"));
process(new ObjectMapper().readTree("true"));
    }
}
