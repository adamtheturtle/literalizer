import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode ZKV = new ObjectMapper().readTree("{\"a\": 1}");
    }
}
