class Main {
    public static void main() {
var my_data = new String[]{
    // strings stay data
    "https://example.org/a/*b*/",  // URL annotation
    "escaped quote: \" // still data",
    "backslash: \\",  // outside the string
    "/* not a comment */"
};
    }
}
