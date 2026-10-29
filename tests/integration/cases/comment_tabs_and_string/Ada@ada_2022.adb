with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- before	line
        AEntry ("value", AStr ("left" & Character'Val(9) & "right"))  -- inline	line
        -- after	line
    ];
begin
    null;
end Main;
