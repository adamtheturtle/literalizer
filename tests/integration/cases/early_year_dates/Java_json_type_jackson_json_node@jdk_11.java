import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"date\": \"0099-05-27\", \"naive\": \"0001-01-01T12:30:00Z\", \"recent\": \"2024-05-27T10:00:00Z\"}");
    }
}
