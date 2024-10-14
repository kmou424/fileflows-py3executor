/**
 * @description Executes any .py file using python3. Supports parameters and setting Flow variables.
 * @param {string} PyFile Path to the .py file
 * @param {string} Args Parameters in key-value pair format, formatted as [KEY=VALUE], allowing multiple settings, e.g., [WORKDIR=/mnt/workdir] [TEMP={temp}]
 * @output Success
 */
function Script(PyFile, Args)
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

    return 1;
}
