with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("i32_below", AInt (-2147483649)),
        AEntry ("i32_minimum", AInt (-2147483648)),
        AEntry ("i32_above", AInt (-2147483647)),
        AEntry ("i32_maximum", AInt (2147483647)),
        AEntry ("i32_over", AInt (2147483648)),
        AEntry ("i64_minimum", AInt (-9223372036854775808)),
        AEntry ("i64_maximum", AInt (9223372036854775807))
    ];
begin
    null;
end Main;
