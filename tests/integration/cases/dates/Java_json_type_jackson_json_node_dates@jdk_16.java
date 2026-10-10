import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"date\": \"2024-01-15\", \"datetime\": \"2024-01-15T12:30:00+00:00\"}");
    }
}
