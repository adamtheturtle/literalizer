import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode userObj = new ObjectMapper().readTree("{\"_\": \"_\"}");
JsonNode my_data = new ObjectMapper().readTree("{\"_\": \"_\"}");
    }
}
