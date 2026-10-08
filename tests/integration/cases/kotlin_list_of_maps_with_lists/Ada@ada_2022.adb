with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("a", AList'[AInt (1)])],
        AMap'[AEntry ("a", AList'[AInt (2)])]
    ];
begin
    null;
end Main;
