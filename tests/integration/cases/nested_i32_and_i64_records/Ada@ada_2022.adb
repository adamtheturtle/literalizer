with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AMap'[AEntry ("value", AInt (1))]],
        AList'[AMap'[AEntry ("value", AInt (1099511627776))]]
    ];
begin
    null;
end Main;
