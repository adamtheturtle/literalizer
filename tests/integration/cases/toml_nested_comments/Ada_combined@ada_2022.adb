with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- About the first dotted key.
        -- About the second dotted key.
        AEntry ("dotted", AMap'[AEntry ("first", AInt (1)), AEntry ("second", AInt (2))]),
        AEntry ("plain", AInt (3)),  -- About the plain key.
        -- Inside the table.
        AEntry ("table", AMap'[AEntry ("inner", AInt (4))]),
        -- Before the first entry.
        -- Before the second entry.
        AEntry ("entries", AList'[AMap'[AEntry ("name", AStr ("one"))], AMap'[AEntry ("name", AStr ("two"))]])
    ];
begin
    my_data := AMap'[
        -- About the first dotted key.
        -- About the second dotted key.
        AEntry ("dotted", AMap'[AEntry ("first", AInt (1)), AEntry ("second", AInt (2))]),
        AEntry ("plain", AInt (3)),  -- About the plain key.
        -- Inside the table.
        AEntry ("table", AMap'[AEntry ("inner", AInt (4))]),
        -- Before the first entry.
        -- Before the second entry.
        AEntry ("entries", AList'[AMap'[AEntry ("name", AStr ("one"))], AMap'[AEntry ("name", AStr ("two"))]])
    ];
end Main;
