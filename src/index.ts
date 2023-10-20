import { Command } from "commander";
import { exec } from "child_process";
const figlet = require("figlet");
const fs = require("fs");
const readline = require("readline");
const path = require("path");

console.log(figlet.textSync("GPX CLI", { horizontalLayout: "full" }));

const program = new Command();

program
.version("1.0.0")
.description("An example CLI for managing a directory")
.option("-r, --reorder <value>", "Reorder GPX files in a directory")
.option("-f, --format_date <value>", "Format date of 1 gpx file")
.option("-d, --densify <value>", "Densify GPX files in a directory")
.parse(process.argv);

const options = program.opts();

const listDirContents = async (filepath: string, extensionPattern: string) => {
  try {
    const files = await fs.promises.readdir(filepath);
    const filteredFiles = files.filter((file: string) => file.endsWith(extensionPattern));
    const detailedFilesPromises = filteredFiles.map(async (file: string) => {
      let fileDetails = await fs.promises.lstat(path.resolve(filepath, file));
      const { size, birthtime } = fileDetails;
      return { filename: file, "size(KB)": size, created_at: birthtime };
    });
    const detailedFiles = await Promise.all(detailedFilesPromises);
    console.table(detailedFiles);
  } catch (error) {
    console.error("Error occurred while reading the directory!", error);
  }
}

const main = async () => {
  if (options.reorder) {
    const filepath = typeof options.reorder === "string" ? options.reorder : __dirname;
    await listDirContents(filepath, ".gpx");
  
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
  
    rl.question("Do you want to continue? (y/n): ", (answer: string) => {
      if (answer.toLowerCase() === "y") {
        console.log("Reordering GPX files...");
        const pythonScript = path.join(__dirname, "order-gpx-points.py");
        exec(`python3 ${pythonScript} ${options.reorder}`, (error, stdout, stderr) => {
          if (error) {
            console.error(`Error: ${error.message}`);
            return;
          }
          console.log(stdout);
        });
      } else {
        console.log("Operation canceled.");
      }
      rl.close();
    });
  }
  
  if (options.format_date) {
    const pythonScript = path.join(__dirname, "format-gpx-dates.py");
    exec(`python3 ${pythonScript} ${options.format_date}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return;
      }
      console.log(stdout);
    });
  }

  if (options.densify) {
    const filepath = typeof options.densify === "string" ? options.densify : __dirname;
    await listDirContents(filepath, ".gpx");
  
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
  
    rl.question("Do you want to continue? (y/n): ", (answer: string) => {
      if (answer.toLowerCase() === "y") {
        console.log("Densifying GPX files...");
        const pythonScript = path.join(__dirname, "densify-gpx.py");
        const child = exec(`python3 ${pythonScript} ${options.densify}`, (error, stdout, stderr) => {
          if (error) {
            console.error(`Error: ${error.message}`);
            return;
          }
        });
        child.stdout?.pipe(process.stdout);
      } else {
        console.log("Operation canceled.");
      }
      rl.close();
    });
  }
}

main();
