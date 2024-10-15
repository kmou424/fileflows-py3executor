/**
 * @description Executes any .py file using python3. Supports parameters and setting Flow variables.
 * @param {string} PyFile Path to the .py file
 * @param {string} Args Parameters in key-value pair format, formatted as [KEY=VALUE], allowing multiple settings, e.g., [WORKDIR=/mnt/workdir] [TEMP={temp}]
 * @param {string} SetWorkingFile Path to the file to set as the working file. Supports parameters in the format of [KEY] to replace with Flow variables at end of execution.
 * @output Success
 */
function Script(PyFile, Args, SetWorkingFile)
{
    let process = Flow.Execute({
        command: "/usr/bin/python3",
        workingDirectory: Flow.TempPath,
        argumentList: [PyFile, JSON.stringify({
            HelperArgs: Args,
            FlowArgs: JSON.stringify(Variables)
    })]
    });

    if (process.exitCode != 0) {
        Logger.ELog("Failed on " + process.exitCode);
        return -1;
    }

    if (process.standardOutput) {
        let stdout = String(process.standardOutput).trim().split("\n")
        let export_vars = JSON.parse(stdout[stdout.length - 1]);
        for (let key in export_vars) {
            Variables[key] = export_vars[key];
        }
    }

    if (process.starndardError)
        Logger.ILog("error: ", process.starndardError);

    if (SetWorkingFile && SetWorkingFile != "") {
        let workingFile = String(SetWorkingFile);
        let args = extractArgs(workingFile);
        Logger.ILog("Args found in SetWorkingFile: " + args);
        if (args.length != 0) {
            args.forEach(arg => {
                workingFile = workingFile.replace('['+arg+']', Variables[arg]);
            });
        }
        Flow.SetWorkingFile(workingFile)
    }

    return 1;
}

function extractArgs(input)
{
    const regex = /\[(.*?)\]/g;

    const results = [];
    let match;

    while ((match = regex.exec(input)) !== null) {
        results.push(match[1]);
    }

    return results;
}
