with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("minimum", AInt (-2147483648)),
        AEntry ("neighbor", AInt (-2147483647)),
        AEntry ("maximum", AInt (2147483647)),
        AEntry ("nested", AList'[AInt (-2147483648)])
    ];
begin
    null;
end Main;
