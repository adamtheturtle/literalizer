import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static class ThingType_ { Object go(Object arg0) { return null; } }
static ThingType_ thing = new ThingType_();
    public static void main() throws Exception {
var my_data = thing.go(new ObjectMapper().readTree("[]"));
    }
}
