import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"morning\": \"09:30:00\", \"afternoon\": \"14:15:00\", \"evening\": \"23:59:59\"}");
    }
}
