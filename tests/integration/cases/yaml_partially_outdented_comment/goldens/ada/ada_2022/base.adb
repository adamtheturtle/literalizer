with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[
            AEntry ("b", AList'[AInt (1)]),
            -- Outdented from the sequence, so the inner mapping claims this.
            AEntry ("c", AInt (2))
        ]),
        -- Outdented from the inner mapping too, so the root claims this.
        AEntry ("d", AInt (3))
    ];
begin
    null;
end Main;
