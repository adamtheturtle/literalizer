with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AList'[AMap'[AEntry ("item", AList'[AInt (1)])]]),
        AEntry ("b", AList'[AMap'[AEntry ("item", AList'[AInt (2)])]])
    ];
begin
    null;
end Main;
