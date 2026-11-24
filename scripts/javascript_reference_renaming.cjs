const value = require("./renamed_data.cjs");

if (value.primary !== value.repeated[0]) {
    throw new Error("Repeated references must point to the same object");
}

process.stdout.write(JSON.stringify(value));
