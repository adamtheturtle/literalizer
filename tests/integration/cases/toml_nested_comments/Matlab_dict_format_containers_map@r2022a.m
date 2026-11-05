my_data = containers.Map({'dotted', 'plain', 'entries', 'table'}, {
    % About the first dotted key.
    % About the second dotted key.
    containers.Map({'first', 'second'}, {1, 2}),
    3,  % About the plain key.
    % Before the first entry.
    % Before the second entry.
    {{containers.Map({'name'}, {"one"}), containers.Map({'name'}, {"two"})}},
    % Inside the table.
    containers.Map({'inner'}, {4})
});
