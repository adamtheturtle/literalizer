with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("values", AList'[AInt (1), AInt (2147483648)])
    ];
begin
    null;
end Main;
