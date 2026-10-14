with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("quote""backslash\", AInt (1)),
        AEntry ("line" & Character'Val(10) & "break", AInt (2)),
        AEntry ("$(literal)${text}", AInt (3)),
        AEntry ("RStr prefix", AInt (4))
    ];
begin
    null;
end Main;
