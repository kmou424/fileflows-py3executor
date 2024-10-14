# FileFlows Python 3 Executor

This project provides a custom executor for Python 3 support in FileFlows, built upon the JavaScript executor provided by FileFlows. It leverages JavaScript code to execute Python implementations seamlessly.

## How to Use

Follow these steps to set up the Python 3 executor:

### Step 1: Set Up JavaScript Script in FileFlows

1. Open the FileFlows console and navigate to the **Scripts** section.
2. Add a new JavaScript script and copy the contents of `py3executor.js` from this repository into the script editor.
3. Save the script with name `Python 3 Executor`.

### Step 2: Prepare Your Python Environment

1. Create a new directory to store your Python 3 scripts.
2. Place `py3executor.py` in that directory. 
   - **Note:** If you are using the Docker version of FileFlows, ensure to mount this directory to the container.

### Step 3: Create Your Python Script

1. In the directory created in Step 2, create a new Python script (e.g., `hello.py`) with the following content:

   ```python
   import os
   # Import the py3executor module
   from py3executor import execute, Helper, Flow

   def main():
       # Get the temporary directory from Flow variables. Reference: https://fileflows.com/docs/guides/variables
       temp_dir = Flow.get_variable('temp')
       # Retrieve the NAME argument from the flow arguments.
       name = Helper.get_arg('NAME', force=True)

       files = os.listdir(temp_dir)
       print(files)

       print('Hello, {}!'.format(name))

       # Set the export variable SCRIPT_RESULT=OK.
       # This variable will be passed to the JS script and will be available in the next sub-flow.
       Flow.set_export_var('SCRIPT_RESULT', 'OK')

   if __name__ == '__main__':
       # Call execute from py3executor to ensure correct flow with the JS script.
       # The input arguments will be parsed in the execute function.
       # The Flow variables will be passed to the JS script at the end of the execute function.
       execute(main)
   ```

### Step 4: Create a Flow in FileFlows

1. In FileFlows, create a new Flow.
2. Add a sub-flow 'Python 3 Executor' from the Scripts section.
3. Fill in the `PyFile` field with the full path to `hello.py` (or the container path if using Docker).
4. Fill in the `Args` field with the arguments to pass to the script, such as `[NAME=your_name]`.
5. Manually trigger the flow to see the output.

Enjoy!