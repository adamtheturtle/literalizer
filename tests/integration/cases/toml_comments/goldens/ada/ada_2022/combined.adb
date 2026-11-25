with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- before
        AEntry ("answer", AInt (42)),  -- inline
        AEntry ("plain", AStr ("ok"))
        -- trailing
    ];
begin
    my_data := AMap'[
        -- before
        AEntry ("answer", AInt (42)),  -- inline
        AEntry ("plain", AStr ("ok"))
        -- trailing
    ];
end Main;
