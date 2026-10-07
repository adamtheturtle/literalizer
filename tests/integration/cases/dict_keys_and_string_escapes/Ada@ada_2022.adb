with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("plain", AList'[AInt (1), AInt (2)]),
        AEntry ("with-dash", AStr ("a" & Character'Val(10) & "b"))
    ];
begin
    null;
end Main;
