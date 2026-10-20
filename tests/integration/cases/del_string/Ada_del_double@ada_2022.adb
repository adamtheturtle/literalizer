with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("x", AStr ("" & Character'Val(127)))
    ];
begin
    null;
end Main;
