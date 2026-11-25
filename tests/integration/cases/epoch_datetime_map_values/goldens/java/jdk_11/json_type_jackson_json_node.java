import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"within_i32\": \"2024-01-15T12:00:00Z\", \"beyond_i32\": \"2099-06-15T08:30:00Z\"}");
    }
}
