with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("b", AList'[AInt (1), AInt (2), AInt (3)])])
    ];
begin
    null;
end Main;
