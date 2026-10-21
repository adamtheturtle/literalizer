with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AList'[AList'[AInt (1), AInt (2)]]),
        AEntry ("b", AList'[AList'[AInt (3)]])
    ];
begin
    null;
end Main;
