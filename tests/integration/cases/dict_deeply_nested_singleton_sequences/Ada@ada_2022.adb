with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("deep", AList'[AList'[AList'[AList'[AInt (1)]]]])
    ];
begin
    null;
end Main;
