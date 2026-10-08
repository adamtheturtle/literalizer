with A_Stub; use A_Stub;
procedure Main is
    procedure F (Value : A_Val) is begin null; end F;
    x : A_Val := AList'[
        AList'[
            AInt (1),
            AInt (2)
        ],
        AList'[
            AInt (3),
            AInt (4)
        ]
    ];
begin
    F(value => AList'[
        AList'[
            x
        ]
    ]);
end Main;
