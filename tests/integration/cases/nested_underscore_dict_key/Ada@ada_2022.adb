with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("outer", AList'[AMap'[AEntry ("_", AInt (1))]])
    ];
begin
    null;
end Main;
