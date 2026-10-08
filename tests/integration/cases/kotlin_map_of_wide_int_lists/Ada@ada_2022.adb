with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AList'[AInt (4294967296), AInt (4294967297)])
    ];
begin
    null;
end Main;
