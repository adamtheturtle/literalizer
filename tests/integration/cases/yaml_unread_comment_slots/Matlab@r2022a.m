my_data = struct(
    'flow', {{
        1,
        % After the first element.
        2
    }},
    % Between the key and its value.
    'gap', 3,
    % On the block scalar header.
    'block', sprintf('%s%s', "Text.", char(10)),
    'anchored', 4,
    'alias', 4
    % On the alias.
);
