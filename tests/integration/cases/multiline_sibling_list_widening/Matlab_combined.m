my_data = struct(
    'omap_value', struct('first', 1),
    'sibling_lists', struct('numbers', {{1, 2}}, 'strings', {{"x", "y"}}),
    'ref_marker_present', {{"$keep", "z"}}
);
my_data = struct(
    'omap_value', struct('first', 1),
    'sibling_lists', struct('numbers', {{1, 2}}, 'strings', {{"x", "y"}}),
    'ref_marker_present', {{"$keep", "z"}}
);
