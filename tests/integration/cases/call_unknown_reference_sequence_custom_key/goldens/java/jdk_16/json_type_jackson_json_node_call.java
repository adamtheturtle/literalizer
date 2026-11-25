import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object process(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode untypedValue = new ObjectMapper().readTree("[]");
process(new ObjectMapper().readTree("[{\"@reference\": \"untyped_value\"}, {\"@reference\": \"untyped_value\"}]"));
    }
}
