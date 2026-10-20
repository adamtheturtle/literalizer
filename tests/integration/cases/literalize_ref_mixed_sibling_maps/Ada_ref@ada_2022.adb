with A_Stub; use A_Stub;
procedure Main is
    actual : A_Val := AInt (42);
    my_data : A_Val := AList'[
        AMap'[AEntry ("$ref", AInt (1))],
        AMap'[AEntry ("$ref", ANull)],
        actual
    ];
begin
    null;
end Main;
