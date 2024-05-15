import proactive

# Create the ProActive scheduler client
client = proactive.ProActiveSchedulerClient('https://try.activeeon.com:8080/automation-dashboard')

# Login to the server
client.login('username', 'password')

# Create the main workflow
main_workflow = client.create_workflow('MainWorkflow')

# Task2
task2 = client.create_python_task('Task2', 'implementation_A.py')
task2.set_python_command("implementation_A.py")
task2.add_python_script_parameter("value", 0.2)
main_workflow.add_task(task2)

# Create Workflow2 subworkflow
workflow2 = client.create_workflow('Workflow2')

# Task5 in Workflow2
task5 = client.create_python_task('Task5', 'implementation_C.py')
task5.set_python_command("implementation_C.py")
workflow2.add_task(task5)

# Task6 in Workflow2
workflow3 = client.create_workflow('Workflow3')

# Task7 in Workflow3
task7 = client.create_python_task('Task7', 'implementation_D.py')
task7.set_python_command("implementation_D.py")
workflow3.add_task(task7)

# Task8 in Workflow3
task8 = client.create_python_task('Task8', 'implementation_E.exe')
task8.set_python_command("implementation_E.exe")
workflow3.add_task(task8)

# Task9 in Workflow3
task9_w3 = client.create_python_task('Task9', 'implementation_F.exe')
task9_w3.set_python_command("implementation_F.exe")
workflow3.add_task(task9_w3)

# Conditional control flow in Workflow3
task7.add_condition(task9_w3, "p > 1")
task7.add_condition(task8, "p < 10")

# Add Workflow3 to Task6 in Workflow2
task6 = client.create_subworkflow_task('Task6', workflow3)
task6.add_subworkflow_parameter("p", 4)
workflow2.add_task(task6)

# Control flow in Workflow2
workflow2.connect_tasks(task5, task6)
workflow2.connect_tasks(task6, task5)

# Add Workflow2 to Task1 in MainWorkflow
task1 = client.create_subworkflow_task('Task1', workflow2)
main_workflow.add_task(task1)

# Task3 in MainWorkflow
task3 = client.create_python_task('Task3', 'implementation_B.py')
task3.set_python_command("implementation_B.py")
main_workflow.add_task(task3)

# Create SubWorkflow subworkflow
sub_workflow = client.create_workflow('SubWorkflow')

# Task10 in SubWorkflow
task10 = client.create_java_task('Task10', 'implementation_F.java')
task10.set_java_command("implementation_F.java")
sub_workflow.add_task(task10)

# Task9 in SubWorkflow
task9_sw = client.create_python_task('Task9', 'implementation_F.py')
task9_sw.set_python_command("implementation_F.py")
sub_workflow.add_task(task9_sw)

# Task11 in SubWorkflow
task11 = client.create_java_task('Task11', 'implementation_G.java')
task11.set_java_command("implementation_G.java")
sub_workflow.add_task(task11)

# Control flow in SubWorkflow
sub_workflow.connect_tasks(task10, task9_sw)
sub_workflow.connect_tasks(task9_sw, task11)

# Add SubWorkflow to Task4 in MainWorkflow
task4 = client.create_subworkflow_task('Task4', sub_workflow)
main_workflow.add_task(task4)

# Control flow in MainWorkflow
main_workflow.connect_tasks(task2, task1)
main_workflow.connect_tasks(task2, task3)
main_workflow.connect_tasks(task3, task4)

# Submit and execute the MainWorkflow
client.submit_workflow(main_workflow)
client.logout()
