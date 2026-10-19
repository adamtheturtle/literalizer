with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("", AInt (1)),
        AEntry ("a" & Character'Val(1) & "b", AInt (2))
    ];
begin
    null;
end Main;
