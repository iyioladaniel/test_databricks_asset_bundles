# Databricks Asset Bundles Demo

This documentatioin demonstrates **Databricks Asset Bundles** - a modern Infrastructure as Code (IaC) approach for managing Databricks resources like jobs, pipelines, notebooks, and configurations in a version-controlled, reproducible way.

## What are Databricks Asset Bundles?

Databricks Asset Bundles allow you to:
- **Version control** your Databricks resources (jobs, pipelines, notebooks)
- **Deploy consistently** across development, staging, and production environments
- **Collaborate effectively** with infrastructure as code principles
- **Automate deployments** with CI/CD pipelines

## Project Structure

```
my_project/
├── databricks.yml                    # Main bundle configuration
├── resources/                        # Resource definitions
│   ├── my_project.job.yml      # Job configuration
│   └── my_project.pipeline.yml # Pipeline configuration
├── src/                              # Source code
│   ├── notebook.ipynb               # Notebook for job task
│   ├── dlt_pipeline.ipynb           # Delta Live Tables pipeline
│   └── my_project/
│       ├── __init__.py
│       └── main.py                  # Python wheel entry point
└── requirements-dev.txt             # Development dependencies
```

## Quick Start Guide

### 1. Prerequisites

Install the Databricks CLI using one of these methods:

**Using pip (Python):**
```bash
pip install databricks-cli
```

**Using PowerShell (Windows):**
```powershell
winget install Databricks.CLI
```

**Using apt (Ubuntu/Debian):**
```bash
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
```

**Using Homebrew (macOS):**
```bash
brew tap databricks/tap
brew install databricks
```

### 2. Authentication

Authenticate to your Databricks workspace:
```bash
databricks configure
```

### 3. Initialize a New Bundle (Optional)

If you're creating a new project from scratch, you can initialize a bundle:
```bash
databricks bundle init
```

Choose the **default-python** template when prompted. This creates the same structure as this demo project.

### 4. Validate Configuration

Before deploying, validate your bundle configuration:
```bash
databricks bundle validate
```
This checks for syntax errors and configuration issues.

### 5. Deploy to Development

Deploy a development copy of this project:
```bash
databricks bundle deploy --target dev
```

**What happens during deployment:**
- Resources get prefixed with `[dev yourname]` for isolation
- Job schedules are automatically paused in development mode
- A Python wheel is built and uploaded from your source code
- Job and pipeline resources are created in your workspace

### 6. Deploy to Production

For production deployment:
```bash
databricks bundle deploy --target prod
```

**Production differences:**
- No resource name prefixes
- Schedules remain active
- Stricter permissions and configurations

### 7. Run Jobs and Pipelines

Execute specific resources by their KEY (resource identifier):

**Run the job:**
```bash
databricks bundle run my_project_job
```

**Run the pipeline:**
```bash
databricks bundle run my_project_pipeline
```

**Run with specific target (if not using default):**
```bash
databricks bundle run my_project_job --target prod
```

**Run with no specific resource (shows available options):**
```bash
databricks bundle run
```

**Run with job parameters:**
```bash
databricks bundle run my_project_job -- --param1 value1 --param2 value2
```

**Run pipeline with refresh options:**
```bash
databricks bundle run my_project_pipeline --refresh-all
```
## Configuration Files Explained

### `databricks.yml` - Main Bundle Configuration

This is the central configuration file that defines your bundle:

```yaml
bundle:
  name: my_databricks_project
  uuid: 12345678-1234-1234-1234-123456789abc

include:
  - resources/*.yml    # Include all resource definition files

targets:
  dev:                # Development environment
    mode: development # Enables dev-specific features (prefixed names, paused schedules)
    default: true
    workspace:
      host: https://adb-1234567890123456.7.azuredatabricks.net

  prod:               # Production environment
    mode: production
    workspace:
      host: https://adb-1234567890123456.7.azuredatabricks.net
      root_path: /Workspace/Users/your.email@company.com/.bundle/${bundle.name}/${bundle.target}
    permissions:
      - user_name: your.email@company.com
        level: CAN_MANAGE
```

### `resources/my_project.job.yml` - Job Definition

Defines a multi-task job with dependencies:

```yaml
resources:
  jobs:
    my_databricks_job:
      name: my_databricks_job
      
      trigger:                    # Scheduled execution
        periodic:
          interval: 1
          unit: DAYS
      
      tasks:
        - task_key: notebook_task           # Task 1: Run notebook
          notebook_task:
            notebook_path: ../src/notebook.ipynb
            
        - task_key: refresh_pipeline        # Task 2: Refresh pipeline (depends on Task 1)
          depends_on:
            - task_key: notebook_task
          pipeline_task:
            pipeline_id: ${resources.pipelines.my_databricks_pipeline.id}
            
        - task_key: main_task              # Task 3: Run Python wheel (depends on Task 2)
          depends_on:
            - task_key: refresh_pipeline
          python_wheel_task:
            package_name: my_databricks_project
            entry_point: main
          libraries:
            - whl: ../dist/*.whl           # References built Python package
      
      job_clusters:                        # Cluster configuration
        - job_cluster_key: job_cluster
          new_cluster:
            spark_version: 15.4.x-scala2.12
            node_type_id: Standard_D3_v2
            autoscale:
              min_workers: 1
              max_workers: 4
```

### `resources/my_project.pipeline.yml` - Pipeline Definition

Defines a Delta Live Tables (DLT) pipeline:

```yaml
resources:
  pipelines:
    my_databricks_pipeline:
      name: my_databricks_pipeline
      catalog: usas_d                                    # Target catalog
      schema: my_project_${bundle.target}              # Dynamic schema based on target
      libraries:
        - notebook:
            path: ../src/dlt_pipeline.ipynb           # DLT notebook source
      configuration:
        bundle.sourcePath: ${workspace.file_path}/src # Source code location
```

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `databricks bundle init` | Initialize a new bundle project |
| `databricks bundle validate` | Validate bundle configuration |
| `databricks bundle deploy --target dev` | Deploy to development |
| `databricks bundle deploy --target prod` | Deploy to production |
| `databricks bundle run <job_name>` | Run specific job (uses default target) |
| `databricks bundle run <pipeline_name>` | Run specific pipeline (uses default target) |
| `databricks bundle run <resource> --target <env>` | Run resource in specific environment |
| `databricks bundle destroy --target dev` | Delete all deployed resources |

## Development Workflow

1. **Make changes** to your code, notebooks, or configurations
2. **Validate** the bundle: `databricks bundle validate`
3. **Deploy** to dev: `databricks bundle deploy --target dev`
4. **Test** your resources: `databricks bundle run <resource>`
5. **Iterate** until satisfied
6. **Deploy to production**: `databricks bundle deploy --target prod`

## Key Benefits Demonstrated

- **Environment Isolation**: Separate dev/prod configurations
- **Dependency Management**: Jobs can depend on pipeline completion
- **Infrastructure as Code**: All resources defined in version-controlled YAML
- **Automated Building**: Python packages built and deployed automatically
- **Resource References**: Pipeline IDs dynamically referenced in jobs

## Troubleshooting

**Validation Errors:**
```bash
databricks bundle validate
```

**Check Deployed Resources:**
```bash
databricks bundle summary --target dev
```

**View Logs:**
Check the Databricks workspace under **Workflows** for job execution details.

## Next Steps

- **Set up CI/CD** pipelines for automated deployments
- **Add more complex workflows** with multiple dependencies
- **Integrate with ML workflows** using MLflow
- **Explore advanced bundle features** like shared clusters and permissions

## Additional Resources

- **Official Documentation**: [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- **VS Code Extension**: [Databricks Extension](https://docs.databricks.com/dev-tools/vscode-ext.html) for local development
- **Databricks Connect**: [Setup Guide](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) for local testing
- **Deployment Modes**: [Understanding Dev vs Prod](https://docs.databricks.com/dev-tools/bundles/deployment-modes.html)

---

*This project demonstrates the power of Infrastructure as Code with Databricks, enabling teams to build, deploy, and manage data and ML workloads with confidence and consistency.*
