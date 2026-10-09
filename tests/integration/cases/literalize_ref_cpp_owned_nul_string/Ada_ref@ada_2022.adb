with A_Stub; use A_Stub;
procedure Main is
    shared : A_Val := AStr ("a" & Character'Val(0) & "b");
    my_data : A_Val := AMap'[
        AEntry ("value", shared)
    ];
begin
    null;
end Main;
