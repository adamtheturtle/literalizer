using System.Text.Json.Nodes;
class Check {
static object? make_widget(object? count = null) => null;
static object? consume(object? count = null) => null;
    public static void Main() {
var my_data = make_widget((JsonNode?)(7));
consume(((JsonNode?)my_data)?.DeepClone());
my_data = (JsonNode?)(make_widget((JsonNode?)(13)) != null ?
make_widget((JsonNode?)(13)) // inner
: null); // trailing
consume(((JsonNode?)my_data)?.DeepClone());
    }
}
