with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        --
        -- document heading
        -- before the first entry
        -- after the key
        -- before the value
        AEntry ("counts", AList'[
            -- before the first item
            AInt (1),  -- inline block after the comma
            -- before the second item
            AInt (2)
            -- trailing inside the array
        ]),  -- after the nested collection
        AEntry ("more", AList'[
            AInt (3),
            --
            -- block heading
            -- block continuation
            AInt (4)  -- final inline
        ])
        -- trailing inside the object
        -- after the root
        -- after the document
    ];
begin
    my_data := AMap'[
        --
        -- document heading
        -- before the first entry
        -- after the key
        -- before the value
        AEntry ("counts", AList'[
            -- before the first item
            AInt (1),  -- inline block after the comma
            -- before the second item
            AInt (2)
            -- trailing inside the array
        ]),  -- after the nested collection
        AEntry ("more", AList'[
            AInt (3),
            --
            -- block heading
            -- block continuation
            AInt (4)  -- final inline
        ])
        -- trailing inside the object
        -- after the root
        -- after the document
    ];
end Main;
