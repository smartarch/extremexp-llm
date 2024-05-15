import subprocess

# Function to run an external command
def run_command(command):
    result = print(command)
    # print(result.stdout)
    # if result.stderr:
        # print(result.stderr)

# Subworkflow: Task6
def run_task6():
    # Task7
    run_command("python implementation_D.py")  # Running Task7 (implementation_D.py)
    
    # Conditional Flow: Task7 -> Task9 (condition: p > 1)
    p = 4
    if p > 1:
        run_command("implementation_F.exe")  # Running Task9 (implementation_F.exe)
    
    # Conditional Flow: Task7 -> Task8 (condition: p < 10)
    if p < 10:
        run_command("implementation_E.exe")  # Running Task8 (implementation_E.exe)

# Subworkflow: Task1
def run_task1():
    # Task5
    run_command("python implementation_C.py")  # Running Task5 (implementation_C.py)
    
    # Task6 (Subworkflow)
    run_task6()
    
    # Task5 again after Task6
    run_command("python implementation_C.py")  # Running Task5 (implementation_C.py) again

# Subworkflow: Task4
def run_task4():
    # Task10
    run_command("java implementation_F.java")  # Running Task10 (implementation_F.java)
    
    # Task9
    run_command("python implementation_F.py")  # Running Task9 (implementation_F.py)
    
    # Task11
    run_command("java implementation_G.java")  # Running Task11 (implementation_G.java)

# Main Workflow: MainWorkflow
def run_main_workflow():
    # Task2
    run_command("python implementation_A.py")  # Running Task2 (implementation_A.py)
    
    # # Parallel Block
    # from concurrent.futures import ThreadPoolExecutor
    # with ThreadPoolExecutor() as executor:
    #     future_task1 = executor.submit(run_task1)
    #     future_task3 = executor.submit(lambda: run_command("python implementation_B.py"))  # Running Task3 (implementation_B.py)
    #     future_task4 = executor.submit(run_task4)
    #    
    #     # Wait for all parallel tasks to complete
    #     future_task1.result()
    #     future_task3.result()
    #     future_task4.result()
    #
    # # Task4 is already run in parallel block

    run_task1()
    run_command("python implementation_B.py")  # Running Task3 (implementation_B.py)
    run_task4()
    

# Run the main workflow
if __name__ == "__main__":
    run_main_workflow()
