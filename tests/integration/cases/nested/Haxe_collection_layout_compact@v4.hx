class Fixture_nested_Haxe_collection_layout_compact {
    public static function main() {
        final my_data = ([
            "users" => ([(["name" => "Bob", "tags" => (["admin", "user"] : Array<Dynamic>)] : Map<String, Dynamic>), (["name" => "Carol", "tags" => (["guest"] : Array<Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
