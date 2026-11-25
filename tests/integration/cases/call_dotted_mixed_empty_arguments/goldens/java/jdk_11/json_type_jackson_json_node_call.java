import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static class ThingType_ { Object go(Object arg0, Object arg1, Object arg2) { return null; } }
static ThingType_ thing = new ThingType_();
    public static void main() throws Exception {
thing.go(new ObjectMapper().readTree("[]"), new ObjectMapper().readTree("[1]"), new ObjectMapper().readTree("[]"));
thing.go(new ObjectMapper().readTree("[\"text\"]"), new ObjectMapper().readTree("[2]"), new ObjectMapper().readTree("[]"));
thing.go(new ObjectMapper().readTree("[]"), new ObjectMapper().readTree("[\"text\"]"), new ObjectMapper().readTree("[]"));
thing.go(new ObjectMapper().readTree("[\"text\"]"), new ObjectMapper().readTree("[2]"), new ObjectMapper().readTree("[3]"));
    }
}
