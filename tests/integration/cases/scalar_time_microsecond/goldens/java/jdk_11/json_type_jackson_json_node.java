import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"exact_millisecond\": \"09:30:15.123000\", \"sub_millisecond\": \"09:30:15.123456\"}");
    }
}
