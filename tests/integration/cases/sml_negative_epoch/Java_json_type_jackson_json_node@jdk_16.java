import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("[\"1960-01-01T00:00:00+00:00\"]");
    }
}
