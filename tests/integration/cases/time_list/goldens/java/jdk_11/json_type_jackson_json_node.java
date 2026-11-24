import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"times\": [\"09:30:00\", \"17:45:00\", \"23:59:59\"]}");
    }
}
