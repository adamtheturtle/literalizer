import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode shared = new ObjectMapper().readTree("[1, 2]");
JsonNode my_data = new ObjectMapper().readTree("[1, 2]");
    }
}
