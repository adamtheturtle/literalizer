with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("x", AStr ("" & Character'Val(0))),
        AEntry ("y", AStr ("" & Character'Val(0) & "1"))
    ];
begin
    null;
end Main;
