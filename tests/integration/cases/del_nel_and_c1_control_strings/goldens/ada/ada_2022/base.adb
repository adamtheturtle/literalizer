with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("del", AStr ("a" & Character'Val(127) & "b")),
        AEntry ("nel", AStr ("a" & Character'Val(194) & Character'Val(133) & "b")),
        AEntry ("c1", AStr ("a" & Character'Val(194) & Character'Val(159) & "b"))
    ];
begin
    null;
end Main;
