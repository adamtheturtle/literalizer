with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- A JSONC input case with both comment forms.
        AEntry ("url", AStr ("https://example.org/a/*b*/")),  -- detail
        -- continued
        AEntry ("count", AInt (2))  -- trailing line comment
    ];
begin
    null;
end Main;
