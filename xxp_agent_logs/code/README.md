# Code generation from workflow specification

Here are the results of generating Python glue code to run the experiment specified via a workflow specification (`.xxp` files).

## Prompt (pure Python)

Generate Python code that will run the experiment specified by the experiment workflow. Use the tools to obtain the specification of the experiment workflow and all the referenced workflows.

If a task has an executable file specified via the `implementation` keyword, use the Python `subprocess` module to run the executable file. Comment the code so it is easy to understand to which task the executable file belongs. If a task has a subworkflow (`subworkflow` keyword), create a function for executing the tasks in the subworkflow.

## Prompt (Proactive SDK)

Generate Python code that will run the experiment specified by the experiment workflow. Use the tools to obtain the specification of the experiment workflow and all the referenced workflows.

Use the ProActive Python Client SDK (`import proactive`) to create corresponding tasks and run them.

## Correct trace

Replace `subprocess.run` with `print` in the generated code to safely execute it.

### [Artificial workflow](/examples/artificial_workflow/)

```shell
implementation_A.py  # Task 2
# PARALLEL_1 (branch 1)
implementation_C.py  # Task 5 (inside Task 1)
implementation_D.py  # Task 7 (inside Task 1, Task 6)
    # the order of Tasks 8 and 9 can be arbitrary
implementation_F.exe  # Task 9 (inside Task 1, Task 6), p = 4 > 1
implementation_F.exe  # Task 8 (inside Task 1, Task 6), p = 4 < 10
    # Tasks 5 and 6 should repeat in an infinite loop
# PARALLEL_1 (branch 2)
implementation_B.py  # Task 3
implementation_F.java  # Task 10 (inside Task 4)
implementation_F.py  # Task 9 (inside Task 4)
implementation_G.java  # Task 11 (inside Task 4)
# PARALLEL_END_1
```

### [AutoML](/examples/automl_wrong_implementation/)

```shell
ideko_data_retreival.py
random_train_test_split.py
# hyperparameter optimization
grid_search.py
ideko_feature_extraction.py
regression_training.py
regression_evaluation.py
    # here should be a conditional loop back to grid_search.py
user_hyperparameter_selection.py
# training of final model
ideko_feature_extraction.py
regression_training.py
regression_evaluation.py
```