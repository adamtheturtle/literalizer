import io.circe.Json
object Fixture_multiline_string_Scala_json_type_circe {
val my_data: Json = Json.arr(
    Json.fromString("first line\n  indented\n\nlast line"),
    Json.fromString("\nleading newline"),
    Json.fromString(" \t\nleading whitespace"),
    Json.fromString("trailing newline\n"),
    Json.fromString("\nleading and trailing\n"),
    Json.fromString("quotes: \"\"\" ''' ` and backslash: \\"),
    Json.fromString("interpolation: ${value} #{value} #@value #$value $value"),
    Json.fromString("backslash before newline: \\\nnext line"),
    Json.fromString("trailing spaces  \nnext"),
    Json.fromString("C++ empty delimiter collision: )\"\nvalue"),
    Json.fromString("C++ first fallback collision: )\" and )x\"\nvalue"),
    Json.fromString("C++ second fallback collision: )\" and )x\" and )x0\"\nvalue"),
    Json.fromString("Rust delimiter collision: \"#\nvalue"),
    Json.fromString("Lua delimiter collision: ]]\nvalue"),
    Json.fromString("Swift delimiter collision: \"\"\"#\nvalue"),
    Json.fromString("Swift interpolation collision: \\#(value)\nvalue"),
    Json.fromString("Ruby fallback interpolation  \n#{expression} #@instance #$global"),
    Json.fromString("NUL followed by a digit: \u00007"),
    Json.fromString("carriage\rreturn"),
)
}
