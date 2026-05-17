class Fixture_literalize_ref_default_nested_Haxe_ref_default {
    public static function main() {
        final item_var = ([
            "_" => "_",
        ] : Map<String, Dynamic>);
        final my_data = ([
            "items" => ([item_var, (["fallback" => "value"] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
