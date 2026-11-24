with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("value", AList'[])],
        AMap'[AEntry ("value", AList'[AInt (1)])]
    ];
begin
    null;
end Main;
