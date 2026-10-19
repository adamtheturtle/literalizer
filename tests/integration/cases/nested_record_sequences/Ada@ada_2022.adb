with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AMap'[AEntry ("a", AInt (1))]],
        AList'[AMap'[AEntry ("a", AInt (2))]]
    ];
begin
    null;
end Main;
