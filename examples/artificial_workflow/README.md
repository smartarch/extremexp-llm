# Artificial workflow example

## Prompt

Read through the specification of the experiment workflow including all its subworkflows (recursively) and parent workflows.
Create a list of all tasks that are implemented in Python (`.py` file extension). Write the list in format: "<WorkflowName>.<TaskName>: <ImplementationFile>".
Produce only the list of all tasks that are implemented in Python exaclty in the defined format without any additional comments.

### Follow up

Are you sure that you analyzed the specification of the whole workflow and all its subworkflows? If not, go through the specification once more and create a list of the tasks implemented in Python that you previously forgot. Keep the same format of the output and do not include tasks that you already listed.

## Expected result

```txt
Task2: implementation_A.py
Task3: implementation_B.py
Task5: implementation_C.py
Task7: implementation_D.py
Task9: implementation_F.py
```

Note that the workflow names might be different for assembled and expanded workflows so we don't include them here in the expected results. Still, it might be interesting to observe the workflow names listed by the Agent.

## Variants

1. Separate `xxp` files divided to packages (`examples/artificial_workflow/1_config.yaml`).
2. Assembled `xxp` workflows -> information from parent workflow are copied to the assembled workflow, nested specification is separated to the subworkflow files, packages are not necessary anymore (`examples/artificial_workflow/2_config.yaml`).
3. 1. with list of all packages and workflows in the initial prompt.
4. 2. with list of all workflows in the initial prompt.
5. Expanded workflow: one `xxp` file with nested subworkflows (`examples/artificial_workflow/5_config.yaml`).

Note: Variants 3 and 4 are not implemented yet (and 1 and 2 perform well enough in this example, so 3 and 4 were not necessary).

## Results (`gpt-4-0125-preview`)

### Found implementations

✅ = during first prompt, ☑️ = during follow up, ❌ = no  
Hallucinations = number of wrong results (non-existent tasks or tasks not in Python)

| Variant | T2 | T3 | T5 | T7 | T9 | Hallucinations |
|---------|----|----|----|----|----|----------------| 
| 1       | ✅ | ✅ | ✅ | ✅ | ✅ | 0 |
| 2       | ✅ | ✅ | ✅ | ✅ | ✅ | 0 |
| 5       | ✅ | ✅ | ☑️ | ✅ | ✅ | 0 |

#### Notes:

* Variant1 Repeated `Task9` on follow up.
* Variant2 Repeated `Task5`, `Task7` and `Task9` on follow up.

### Obtained specifications of workflows

✅ = yes, ❌ = no, ➖ = not applicable

|Variant|`MW`|`SW`|`W1`|`W2`|`W3`|`W4`|
|-|-|-|-|-|-|-|
|1|✅|✅|✅|✅|✅|✅|
|2|✅|✅|➖|✅|✅|➖|
|5|✅|➖|➖|➖|➖|➖|


