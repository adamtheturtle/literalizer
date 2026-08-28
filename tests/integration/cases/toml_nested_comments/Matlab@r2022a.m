my_data = struct(
    % About the first dotted key.
    % About the second dotted key.
    'dotted', struct('first', 1, 'second', 2),
    'plain', 3,  % About the plain key.
    % Before the first entry.
    % Before the second entry.
    'entries', {{struct('name', "one"), struct('name', "two")}},
    % Inside the table.
    'table', struct('inner', 4)
);
