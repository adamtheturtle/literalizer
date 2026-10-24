import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("[\"1901-12-13T20:45:51Z\", \"1901-12-13T20:45:52Z\", \"2038-01-19T03:14:07Z\", \"2038-01-19T03:14:08Z\"]");
    }
}
