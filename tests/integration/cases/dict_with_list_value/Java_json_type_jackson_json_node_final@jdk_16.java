import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
final JsonNode my_data = new ObjectMapper().readTree("{\"name\": \"Alice\", \"scores\": [10, 20, 30]}");
    }
}
