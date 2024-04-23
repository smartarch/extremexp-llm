# Artificial workflow example

## Variants

1. Separate `abc` files divided to packages (`examples/artificial_workflow/1_config.yaml`).
2. Assembled `abc` workflows -> information from parent workflow are copied to the assembled workflow, nested specification is separated to the subworkflow files, packages are not necessary anymore (`examples/artificial_workflow/2_config.yaml`).
3. Expanded workflow: one `abc` file with nested subworkflows (`examples/artificial_workflow/3_config.yaml`).

## Goal: List all Python tasks

### Prompt

Read through the specification of the experiment workflow including all its subworkflows (recursively) and parent workflows.
Create a list of all tasks that are implemented in Python (`.py` file extension). Write the list in format: "<WorkflowName>.<TaskName>: <ImplementationFile>".
Produce only the list of all tasks that are implemented in Python exaclty in the defined format without any additional comments.

#### Follow up

Are you sure that you analyzed the specification of the whole workflow and all its subworkflows? If not, go through the specification once more and create a list of the tasks implemented in Python that you previously forgot. Keep the same format of the output and do not include tasks that you already listed.

### Expected result

```txt
Task2: implementation_A.py
Task3: implementation_B.py
Task5: implementation_C.py
Task7: implementation_D.py
Task9: implementation_F.py
```

Note that the workflow names might be different for assembled and expanded workflows so we don't include them here in the expected results. Still, it might be interesting to observe the workflow names listed by the Agent.

### Results (`gpt-4-0125-preview`)

#### Found implementations

✅ = during first prompt, ☑️ = during follow up, ❌ = no  
Hallucinations = number of wrong results (non-existent tasks or tasks not in Python)

| Variant | T2 | T3 | T5 | T7 | T9 | Hallucinations |
|---------|----|----|----|----|----|----------------| 
| 1       | ✅ | ✅ | ✅ | ✅ | ✅ | 0 |
| 2       | ✅ | ✅ | ✅ | ✅ | ✅ | 0 |
| 3       | ✅ | ✅ | ☑️ | ✅ | ✅ | 0 |

##### Notes:

* Variant1 Repeated `Task9` on follow up.
* Variant2 Repeated `Task5`, `Task7` and `Task9` on follow up.

#### Obtained specifications of workflows

✅ = yes, ❌ = no, ➖ = not applicable

|Variant|`MW`|`SW`|`W1`|`W2`|`W3`|`W4`|
|-|-|-|-|-|-|-|
|1|✅|✅|✅|✅|✅|✅|
|2|✅|✅|➖|✅|✅|➖|
|3|✅|➖|➖|➖|➖|➖|

## Goal: identify errors

There is an error in the specification of `Workflow2`. The `END` of the control flow is missing and the tasks `Task5` and `Task6` are connected in a infinite cycle.

### Prompt

Read through the specification of the experiment workflow including all its subworkflows (recursively) and parent workflows.
Identify potential errors in the workflow specification and present a list of them. For each error, report to which task it is related.

Make sure that you read and analyze all the specification files before presenting the list of errors. Only present errors which come from the specifications of the workflows.

#### Follow up

You did not explore the subworkflows of `Workflow1`. You need to explore all the subworkflows recursively.

### Expected result

Report the cyclic control flow between `Task5` and `Task6`. The missing `END` might not be reported as the Agent does not have a full description of the specification DSL.

### Results (`gpt-4-0125-preview`)

#### Errors found

✅ = during first prompt, ☑️ = during follow up, ❌ = no  

| Variant | Cyclic control flow | Reasonable errors / Reported errors |
|---------|----|---|
| 1       | ☑️ | 1/4 + 3/5 |
| 2       | ✅ | 5/6 |
| 3       | ✅ | 4/4 |

* Version1: From the reported errors, it seems that the Agent does not understand the inheritance of workflow specifications. Further investigation is needed whether this can be fixed by updating the prompt (including this information explicitly).

#### Obtained specifications of workflows

✅ = during first prompt, ☑️ = during follow up, ❌ = no, ➖ = not applicable

|Variant|`MW`|`SW`|`W1`|`W2`|`W3`|`W4`|
|-|-|-|-|-|-|-|
|1|✅|✅|✅|☑️|☑️|✅|
|2|✅|✅|➖|✅|✅|➖|
|3|✅|➖|➖|➖|➖|➖|
