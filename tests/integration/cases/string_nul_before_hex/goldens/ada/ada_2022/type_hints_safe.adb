with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("x", AStr ("before" & Character'Val(0) & "after"))
    ];
begin
    null;
end Main;
