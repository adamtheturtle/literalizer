class Fixture_call_powershell_type_literal_arguments_Haxe_float_format_fixed_call {
    public static function main() {
        function capture(nan_value:Dynamic, positive_infinity:Dynamic, negative_infinity:Dynamic, finite_value:Dynamic, date_value:Dynamic, datetime_value:Dynamic, text_value:Dynamic):Dynamic return null;
        capture(Math.NaN, Math.POSITIVE_INFINITY, Math.NEGATIVE_INFINITY, 1.250000, "2024-01-15", "2024-01-15T12:34:56", "[ordinary text]");
    }
}
