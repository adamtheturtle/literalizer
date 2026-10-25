with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("v", AStr ("a" & Character'Val(127) & "b")),
        AEntry ("a" & Character'Val(127) & "b", AInt (1))
    ];
begin
    null;
end Main;
