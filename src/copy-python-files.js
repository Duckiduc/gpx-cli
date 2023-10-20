const fs = require("fs-extra");
const path = require("path");

const sourceDirectory = "src/gpx-data"; // Replace with your source directory
const destinationDirectory = "dist"; // Replace with your destination directory

async function copyPythonFiles() {
  try {
    await fs.ensureDir(destinationDirectory);
    const files = await fs.readdir(sourceDirectory);
    for (const file of files) {
      if (file.endsWith(".py")) {
        await fs.copy(
          path.join(sourceDirectory, file),
          path.join(destinationDirectory, file)
        );
        console.log(`Copied ${file}`);
      }
    }
  } catch (err) {
    console.error("Error copying Python files:", err);
  }
}

copyPythonFiles();
