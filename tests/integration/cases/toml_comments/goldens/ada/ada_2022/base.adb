with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- before
        AEntry ("answer", AInt (42)),  -- inline
        AEntry ("plain", AStr ("ok"))
        -- trailing
    ];
begin
    null;
end Main;
