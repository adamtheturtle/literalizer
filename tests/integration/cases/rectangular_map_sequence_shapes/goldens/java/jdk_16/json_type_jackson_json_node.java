import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"a\": [{\"item\": [1]}], \"b\": [{\"item\": [2]}]}");
    }
}
