#!/usr/bin/env node
// Optional adapter: execute portable base-R scripts with actual R in WebAssembly.
// Install webr@0.6.0 separately; set SAS_TRAINING_WEBR to its package directory.
const path = require('node:path');
const fs = require('node:fs');
const { WebR } = require(process.env.SAS_TRAINING_WEBR || 'webr');

async function main() {
  if (!process.argv[2]) throw new Error('Usage: node tools/run_r_webr.cjs path/to/test.R [args...]');
  const root = path.resolve(__dirname, '..');
  const script = path.resolve(process.argv[2]);
  const relative = path.relative(root, script);
  if (relative.startsWith('..') || path.isAbsolute(relative)) throw new Error('Script must be within this repository.');
  if (!fs.existsSync(script)) throw new Error(`Script not found: ${script}`);
  const r = new WebR({ RArgs: ['--vanilla', '--args', ...process.argv.slice(3)], interactive: false });
  try {
    await r.init();
    let directory = '';
    for (const part of root.split(path.sep).filter(Boolean)) {
      directory += '/' + part;
      try { await r.FS.mkdir(directory); } catch (error) {
        // Parent directories can already exist in the R virtual filesystem.
        await r.FS.lookupPath(directory);
      }
    }
    await r.FS.mount('NODEFS', { root }, root);
    console.log(`Runtime: ${await r.evalRString('R.version.string')} [WebR]`);
    await r.evalRVoid(`
      setwd(${JSON.stringify(path.dirname(script))})
      commandArgs <- local({
        original <- base::commandArgs
        filearg <- ${JSON.stringify('--file=' + script)}
        function(trailingOnly=FALSE) {
          args <- original(trailingOnly=trailingOnly)
          if (trailingOnly) return(args)
          sep <- match('--args', args, nomatch=length(args)+1L)
          append(args, filearg, after=sep-1L)
        }
      })
    `);
    const shelter = await new r.Shelter();
    const captured = await shelter.captureR(
      `tryCatch({ source(${JSON.stringify(script)}, local=.GlobalEnv, chdir=TRUE); TRUE }, error=function(e) { message(conditionMessage(e)); FALSE })`,
      { captureGraphics: false }
    );
    for (const item of captured.output) {
      const value = typeof item.data === 'string' ? item.data : JSON.stringify(item.data);
      if (item.type === 'stdout') process.stdout.write(value + '\n');
      else process.stderr.write(`${item.type}: ${value}\n`);
    }
    const status = await captured.result.toJs();
    if (!status.values[0]) process.exitCode = 1;
    await shelter.purge();
  } finally {
    r.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
