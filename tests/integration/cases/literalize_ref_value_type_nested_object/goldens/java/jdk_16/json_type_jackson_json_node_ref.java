import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode shared = new ObjectMapper().readTree("[1, 2]");
JsonNode build = new ObjectMapper().readTree("[1, 2]");
JsonNode jsonObject = new ObjectMapper().readTree("[1, 2]");
JsonNode jsonAllocator = new ObjectMapper().readTree("[1, 2]");
JsonNode jsonEntries = new ObjectMapper().readTree("[1, 2]");
JsonNode jsonEntry = new ObjectMapper().readTree("[1, 2]");
JsonNode my_data = new ObjectMapper().readTree("{\"field\": [1, 2], \"nested\": [[1, 2], {}], \"build\": [1, 2], \"json_object\": [1, 2], \"json_allocator\": [1, 2], \"json_entries\": [1, 2], \"json_entry\": [1, 2]}");
    }
}
