import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode shared = new ObjectMapper().readTree("\"value\"");
JsonNode my_data = new ObjectMapper().readTree("\"value\"");
    }
}
