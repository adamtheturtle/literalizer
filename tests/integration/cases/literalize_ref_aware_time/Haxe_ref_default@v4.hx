class Fixture_literalize_ref_aware_time_Haxe_ref_default {
    public static function main() {
        final shared_time = "12:30:15+02:00";
        final my_data = ([
            "x" => shared_time,
        ] : Map<String, Dynamic>);
    }
}
