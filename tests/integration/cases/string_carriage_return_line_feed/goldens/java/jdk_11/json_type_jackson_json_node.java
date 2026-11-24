import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"cr\": \"a\\rb\", \"crlf\": \"a\\r\\nb\", \"lf\": \"a\\nb\"}");
    }
}
