import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object make_widget(Object arg0) { return null; }
static Object consume(Object arg0) { return null; }
    public static void main() throws Exception {
var my_data = make_widget(new ObjectMapper().readTree("7"));
consume(my_data);
my_data = new ObjectMapper().readTree("13");
consume(my_data);
    }
}
