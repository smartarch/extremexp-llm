import proactive

# Initialize the ProActive Scheduler Client
gateway = proactive.ProActiveGateway()
gateway.connect('username', 'password', 'https://try.activeeon.com:8443')

# Create a new ProActive Job
job = gateway.createJob()

# Define InputData
input_data = "path/to/InputData"

# Define Task2
task2 = gateway.createPythonTask()
task2.setImplementation("file://implementation_A.py")
task2.addArgument("0.2")
task2.addInputFile(input_data)

# Define Task1
task1 = gateway.createJob()
task1.setName("Task1")

# Define Task5 within Task1
task5 = gateway.createPythonTask()
task5.setImplementation("file://implementation_C.py")

# Define Task6 within Task1
task6 = gateway.createJob()
task6.setName("Task6")

# Define Task7 within Task6
task7 = gateway.createPythonTask()
task7.setImplementation("file://implementation_D.py")

# Define Task8 within Task6
task8 = gateway.createNativeTask()
task8.setImplementation("file://implementation_E.exe")

# Define Task9 within Task6
task9_6 = gateway.createNativeTask()
task9_6.setImplementation("file://implementation_F.exe")

# Define Task6 workflow
task6.addTask(task7)
task6.addTask(task8)
task6.addTask(task9_6)
task6.connectTasks(task7, task9_6, "p > 1")
task6.connectTasks(task7, task8, "p < 10")
task6.connectTasks(task9_6, task6.getEndTask())
task6.connectTasks(task8, task6.getEndTask())

# Define Task1 workflow
task1.addTask(task5)
task1.addTask(task6)
task1.connectTasks(task5, task6)
task1.connectTasks(task6, task5)

# Define Task3
task3 = gateway.createPythonTask()
task3.setImplementation("file://implementation_B.py")

# Define Task4
task4 = gateway.createJob()
task4.setName("Task4")

# Define Task10 within Task4
task10 = gateway.createJavaTask()
task10.setImplementation("file://implementation_F.java")

# Define Task9 within Task4
task9_4 = gateway.createPythonTask()
task9_4.setImplementation("file://implementation_F.py")

# Define Task11 within Task4
task11 = gateway.createJavaTask()
task11.setImplementation("file://implementation_G.java")

# Define Task4 workflow
task4.addTask(task10)
task4.addTask(task9_4)
task4.addTask(task11)
task4.connectTasks(task10, task9_4)
task4.connectTasks(task9_4, task11)
task4.connectTasks(task11, task4.getEndTask())

# Add tasks to the main workflow
job.addTask(task2)
job.addTask(task1)
job.addTask(task3)
job.addTask(task4)

# Define the workflow connections
job.connectTasks(task2, task1)
job.connectTasks(task2, task3)
job.connectTasks(task3, task4)
job.connectTasks(task1, job.getEndTask())
job.connectTasks(task4, job.getEndTask())

# Submit the job to the scheduler
jobId = gateway.submitJob(job)
print("Job submitted with ID:", jobId)

# Disconnect from the ProActive Scheduler
gateway.disconnect()
