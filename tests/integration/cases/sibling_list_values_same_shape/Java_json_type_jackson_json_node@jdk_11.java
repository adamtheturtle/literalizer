import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"test\": [5, [\"compile\", \"test\"]], \"package\": [7, [\"link\", \"test\"]]}");
    }
}
