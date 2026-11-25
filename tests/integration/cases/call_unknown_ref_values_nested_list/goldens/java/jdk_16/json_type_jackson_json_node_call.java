import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object process(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode unknown_value = new ObjectMapper().readTree("[]");
process(new ObjectMapper().readTree("[{\"$ref\": \"unknown_value\"}]"));
    }
}
