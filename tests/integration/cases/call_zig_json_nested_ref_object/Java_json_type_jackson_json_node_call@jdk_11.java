import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume(Object... args) { return null; }
    public static void main() throws Exception {
JsonNode shared = new ObjectMapper().readTree("[1, 2]");
consume(new ObjectMapper().readTree("{\"field\": {\"$ref\": \"shared\"}, \"nested\": [{\"$ref\": \"shared\"}, {}]}"));
    }
}
