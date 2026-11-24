import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode shared = new ObjectMapper().readTree("[1, 2]");
consume(new ObjectMapper().readTree("[{\"$ref\": \"shared\"}, {\"$ref\": \"shared\"}]"));
    }
}
