import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
// leading
JsonNode my_data = new ObjectMapper().readTree("1");
    }
}
