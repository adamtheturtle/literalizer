const siblings = require("./sibling_data.cjs");

const rows = siblings.map((value) => {
    if (Array.isArray(value)) return { kind: "array", value };
    if (value instanceof Map) {
        return { kind: "map", value: Object.fromEntries(value) };
    }
    if (value !== null && Object.getPrototypeOf(value) === Object.prototype) {
        return { kind: "object", value };
    }
    throw new TypeError("Expected an array, map, or plain object");
});

process.stdout.write(JSON.stringify({ rows }));
