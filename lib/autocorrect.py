import shlex
from subprocess import Popen, PIPE
from ai import autoCorrect_query, make_query

fileName = "test.py"

def execute_and_return(cmd):
    """
    Execute the external command and get its exit code, stdout, and stderr.
    Args:
        cmd (str): The command to execute.
    Returns:
        tuple: A tuple containing (exitcode, stdout, stderr).
    """
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode  # Capture the exit code
    return exitcode, out.decode('utf-8'), err.decode('utf-8')  # Decode the output for better readability

def extract_raw_code(code):
    """Extract the raw code by removing unwanted introductory text and triple backtick blocks."""
    if code.startswith("```") and code.endswith("```"):
        return code[3:-3].strip()  # Remove the first and last three characters (triple quotes)
    elif code.startswith("```"):
        return code[3:].strip()
    if code.endswith("```"):
        return code[:-3].strip()
    return code.strip()  # Return the original code if no triple quotes are found

def autoCorrect(solution, file):
    """Overwrites the given file with the corrected solution."""
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(solution)
            print(f"{file} has been rewritten with corrected code.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def get_test_code(filename):
    """Reads the full code of the given file and returns it."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def main():
    # Read the code from the specified file
    test_code = get_test_code(fileName)
    if not test_code:
        print("No test code found.")
        exit(1)

    # Execute the code and capture stdout and stderr
    exit_code, out, err = execute_and_return(f"python {fileName}")
    print(f"Execution Output:\n{out}\n")
    print(f"Execution Errors:\n{err}\n")
    print(f"Exit Code: {exit_code}")

    if exit_code != 0:  # Handle errors if the exit code is non-zero
        print("Error detected. Processing...")
        query = f"Code:\n{test_code}\nError:\n{err}"
        corrected_code = autoCorrect_query(query=query)
        
        # Extract and print the corrected code
        trimmed_corrected_code = extract_raw_code(corrected_code)
        print("Corrected Code:\n", trimmed_corrected_code)
        
        # Save the corrected code back to the file
        autoCorrect(trimmed_corrected_code, fileName)

    elif out.strip():  # Handle non-error output
        query_manual = "if there is any error shown in the output then return true otherwise false, just give me true or false no extra text"
        if_err_query = f"{out}\n{query_manual}"
        if_err = make_query(if_err_query)

        if if_err == "true":
            print("Detected potential error in output. Resolving it...")
            query = f"Code:\n{test_code}\nOutput:\n{out}"
            corrected_code = autoCorrect_query(query=query)
            
            # Extract and print the corrected code
            trimmed_corrected_code = extract_raw_code(corrected_code)
            print("Corrected Code:\n", trimmed_corrected_code)
            
            # Save the corrected code back to the file
            autoCorrect(trimmed_corrected_code, fileName)
    else:
        print("No errors or issues detected in the script.")

if __name__ == "__main__":
    main()
