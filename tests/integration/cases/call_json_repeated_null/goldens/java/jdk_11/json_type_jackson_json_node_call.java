import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode shared = new ObjectMapper().readTree("null");
consume(new ObjectMapper().readTree("{\"left\": {\"$ref\": \"shared\"}, \"nested\": [{\"$ref\": \"shared\"}]}"));
    }
}
