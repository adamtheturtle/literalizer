import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume(Object... args) { return null; }
    public static void main() throws Exception {
JsonNode item = new ObjectMapper().readTree("\"s\"");
consume(item);
    }
}
