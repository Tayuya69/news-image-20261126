// SPDX-License-Identifier: MIT
// Copies the front-page image for 26 November 2026 to the output directory.
// Fully deterministic: a fixed byte copy, no date, no randomness, no network.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoDir, "entry.png"), join(outDir, "entry.png"));

// Post-write read-back verification: re-read the written file and assert
// its bytes equal the repository's entry.png, so a silent partial copy
// can never pass as a successful run.
import { readFileSync } from "node:fs";
const written = readFileSync(join(outDir, "entry.png"));
const source = readFileSync(join(repoDir, "entry.png"));
if (!written.equals(source)) {
  throw new Error("entry.png verification failed: output bytes differ from entry.png");
}
