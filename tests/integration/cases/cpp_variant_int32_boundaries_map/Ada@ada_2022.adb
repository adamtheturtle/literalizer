with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("below", AInt (-2147483649)),
        AEntry ("minimum", AInt (-2147483648)),
        AEntry ("above", AInt (-2147483647)),
        AEntry ("nested", AList'[AInt (0)])
    ];
begin
    null;
end Main;
