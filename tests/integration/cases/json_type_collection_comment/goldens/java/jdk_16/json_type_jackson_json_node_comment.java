import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
// About a.
JsonNode my_data = new ObjectMapper().readTree("{\"a\": 1, \"b\": 2}");
    }
}
