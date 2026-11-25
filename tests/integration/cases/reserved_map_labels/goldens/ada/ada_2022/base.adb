with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("if", AInt (1)),
        AEntry ("then", AInt (2)),
        AEntry ("else", AInt (3)),
        AEntry ("let", AInt (4)),
        AEntry ("in", AInt (5)),
        AEntry ("using", AInt (6)),
        AEntry ("missing", AInt (7)),
        AEntry ("assert", AInt (8)),
        AEntry ("as", AInt (9)),
        AEntry ("Infinity", AInt (10)),
        AEntry ("NaN", AInt (11)),
        AEntry ("merge", AInt (12)),
        AEntry ("Some", AInt (13)),
        AEntry ("toMap", AInt (14)),
        AEntry ("forall", AInt (15)),
        AEntry ("with", AInt (16)),
        AEntry ("ordinary", AInt (17))
    ];
begin
    null;
end Main;
