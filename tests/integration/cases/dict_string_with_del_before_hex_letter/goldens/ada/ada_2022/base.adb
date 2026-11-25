with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("value", AStr ("del" & Character'Val(127) & "d"))
    ];
begin
    null;
end Main;
