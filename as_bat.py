import subprocess

# Define the command to be executed by subprocess
phrase = "01_HelloWorld.exe -p 45 -t 89 and so on"
phrase_to_list = phrase.split()

print("\n*** subprocess.Popen and saving to logfile for further processing ******************")

# Open the logfile.log file and clear its contents
with open("logfile.log", "w") as log:
    pass

# Open the file for appending and save the process output to the log file
with open("logfile.log", "a", encoding="utf-8") as log:
    proc = subprocess.Popen(phrase_to_list, bufsize=0, stdout=subprocess.PIPE, shell=True)

    for byte in iter(lambda: proc.stdout.read(1), b''):
        decoded_byte = byte.decode('utf-8', 'ignore')
        print(decoded_byte, flush=True, end='')
        log.write(decoded_byte)

    proc.stdout.close()
    proc.wait()  # waits for the subprocess to complete
