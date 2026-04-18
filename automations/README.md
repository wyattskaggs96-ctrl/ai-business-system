# Automations

This module handles automated workflows for repetitive tasks like posting content, sending emails, etc.

## Usage

```python
from automations.workflow_runner import WorkflowRunner

runner = WorkflowRunner()
runner.run_daily_post()
```