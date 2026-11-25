with A_Stub; use A_Stub;
procedure Main is
    actual : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AList'[
        AMap'[AEntry ("$ref", AInt (1))],
        AMap'[AEntry ("$ref", ANull)],
        actual
    ];
begin
    null;
end Main;
