with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("$ref", AStr ("ref_x"))],
        AInt (1),
        AInt (2)
    ];
begin
    null;
end Main;
