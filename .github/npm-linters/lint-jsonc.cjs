"use strict";

const fs = require("node:fs");
const { parse, printParseErrorCode } = require("jsonc-parser");

let failed = false;
for (const file of process.argv.slice(2)) {
  const source = fs.readFileSync(file, "utf8");
  const errors = [];
  parse(source, errors, { allowTrailingComma: false });
  for (const error of errors) {
    console.error(`${file}:${error.offset}: ${printParseErrorCode(error.error)}`);
    failed = true;
  }
}

if (failed) process.exitCode = 1;
