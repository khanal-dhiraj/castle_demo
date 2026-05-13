const assert = require("node:assert/strict");
const { test } = require("node:test");
const { reverse } = require("./reverse");

test("reverses a normal word", () => {
  assert.equal(reverse("hello"), "olleh");
});

test("returns empty string when given empty string", () => {
  assert.equal(reverse(""), "");
});
