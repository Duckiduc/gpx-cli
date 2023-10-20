import { Command } from "commander";
import { exec } from "child_process";
const figlet = require("figlet");

const program = new Command();

program
  .version("1.0.0")
  .description("An example CLI for managing a directory")
  .option("-l, --ls  [value]", "List directory contents")
  .option("-m, --mkdir <value>", "Create a directory")
  .option("-t, --touch <value>", "Create a file")
  .option("--reorder <value>", "Reorder GPX files")
  .parse(process.argv);

const options = program.opts();

if (options.reorder) {
  console.log("Reordering GPX files..." + options.reorder);
  // const pythonScript = "gpx_tool.py";
  // exec(`python ${pythonScript} reorder ${options.reorder}`, (error, stdout, stderr) => {
  //   if (error) {
  //     console.error(`Error: ${error.message}`);
  //     return;
  //   }
  //   console.log(stdout);
  // });
}

if (options.process) {
  const pythonScript = "gpx_tool.py";
  exec(`python ${pythonScript} process ${options.process}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return;
    }
    console.log(stdout);
  });
}
