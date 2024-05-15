import proactive

# Initialize the ProActive client
gateway = proactive.ProActiveGateway()
gateway.connect(username="your_username", password="your_password")

# Define tasks
task2 = proactive.createPythonTask(script_path="file://implementation_A.py", parameters={"value": 0.2})
task5 = proactive.createPythonTask(script_path="file://implementation_C.py")
task7 = proactive.createPythonTask(script_path="file://implementation_D.py")
task8 = proactive.createExecutableTask(executable_path="file://implementation_E.exe")
task9 = proactive.createExecutableTask(executable_path="file://implementation_F.exe")
task10 = proactive.createJavaTask(java_class="file://implementation_F.java")
task11 = proactive.createJavaTask(java_class="file://implementation_G.java")

# Define workflows
workflow3 = proactive.createWorkflow(name="Workflow3", tasks=[task7, task8, task9], connections=[
    proactive.createCondition(task7, task9, condition="p > 1"),
    proactive.createCondition(task7, task8, condition="p < 10"),
])
workflow2 = proactive.createWorkflow(name="Workflow2", tasks=[task5, proactive.createSubworkflowTask(workflow3, parameters={"p": 4})])
workflow4 = proactive.createWorkflow(name="Workflow4", tasks=[task10, task9, task11])
subworkflow = proactive.createWorkflow(name="SubWorkflow", base_workflow=workflow4, task_configs={"Task9": task9, "Task11": task11})
workflow1 = proactive.createWorkflow(name="Workflow1", tasks=[task2, proactive.createSubworkflowTask(workflow2)], connections=[
    proactive.createParallelConnection([task2], [proactive.createSubworkflowTask(workflow2), proactive.createTask(task8)], end_parallel_task=proactive.createTask(task9))
])
main_workflow = proactive.createWorkflow(name="MainWorkflow", base_workflow=workflow1, task_configs={"Task3": proactive.createPythonTask(script_path="file://implementation_B.py"), "Task4": proactive.createSubworkflowTask(subworkflow)})

# Submit workflow
jobId = gateway.submitWorkflow(main_workflow)

# Wait for job to complete
gateway.monitorJob(jobId)
results = gateway.getJobResults(jobId)

print(results)
