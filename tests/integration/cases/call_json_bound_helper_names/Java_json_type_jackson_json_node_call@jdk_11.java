import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object process(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode arena = new ObjectMapper().readTree("{\"a\": 1}");
JsonNode ZVal = new ObjectMapper().readTree("{\"a\": 1}");
JsonNode ZKV = new ObjectMapper().readTree("{\"a\": 1}");
process(arena);
process(ZVal);
process(ZKV);
    }
}
