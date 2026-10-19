class Fixture_record_empty_nested_list_Haxe_declaration_style_var {
    public static function main() {
        var my_data = ([
            "a" => ([([1, 2] : Array<Dynamic>), ([3] : Array<Dynamic>)] : Array<Dynamic>),
            "b" => ([([] : Array<Dynamic>), ([1] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
