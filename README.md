# Databricks Asset Bundles Demo Project

This documentation demonstrates **Databricks Asset Bundles** - a modern Infrastructure as Code (IaC) approach for managing Databricks resources like jobs, pipelines, notebooks, and configurations in a version-controlled, reproducible way.

**✨ Features:**
- Complete CI/CD pipeline with GitHub Actions
- Multi-environment deployment (dev/prod)
- **Optimized compute** with shared clusters and serverless pipelines (cost-optimized, quick startup)
- Automated testing and validation
- Service principal authentication for production
- Controlled workspace permissions

## What are Databricks Asset Bundles?

Databricks Asset Bundles allow you to:
- **Version control** your Databricks resources (jobs, pipelines, notebooks)
- **Deploy consistently** across development, staging, and production environments
- **Collaborate effectively** with infrastructure as code principles
- **Automate deployments** with CI/CD pipelines

## Project Structure

```
test_databricks_asset_bundles/
├── .github/
│   └── workflows/                   # CI/CD pipelines
│       ├── ci.yml                  # Continuous Integration
│       └── cd.yml                  # Continuous Deployment
├── databricks.yml                   # Main bundle configuration
├── resources/                       # Resource definitions
│   ├── test_databricks_asset_bundles.job.yml      # Job configuration
│   └── test_databricks_asset_bundles.pipeline.yml # Pipeline configuration
├── src/                            # Source code
│   ├── notebook.ipynb             # Notebook for job task
│   ├── dlt_pipeline.ipynb         # Delta Live Tables pipeline
│   └── test_databricks_asset_bundles/
│       ├── __init__.py
│       └── main.py                # Python wheel entry point
├── tests/                          # Unit tests
│   └── main_test.py
├── requirements-dev.txt            # Development dependencies
├── setup.py                        # Python package configuration
└── README.md                       # This documentation
```

## Quick Start Guide

### 1. Prerequisites

Install the **new Databricks CLI** (required for Asset Bundles):

**⚠️ Important: Use the new CLI, not the old `databricks-cli` package**

**Using the official installer (Recommended):**
```bash
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
```

**Using Homebrew (macOS):**
```bash
brew tap databricks/tap
brew install databricks
```

**Using winget (Windows):**
```powershell
winget install Databricks.CLI
```

**❌ Don't use:** `pip install databricks-cli` (this is the old CLI that doesn't support bundles)

### 2. Authentication

**For Local Development:**
You can authenticate using either the profile-based approach or environment variables:

**Option A: Profile-based (Traditional):**
```bash
databricks configure
```

**Option B: Environment Variables (CI/CD Compatible):**
```bash
export DATABRICKS_HOST=https://your-workspace.azuredatabricks.net
export DATABRICKS_TOKEN=your-token
```

**For CI/CD:**
The pipeline uses environment variables automatically from GitHub Secrets (no manual configuration needed).

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
databricks bundle run test_databricks_asset_bundles_job
```

**Run the pipeline:**
```bash
databricks bundle run test_databricks_asset_bundles_pipeline
```

**Run with specific target (if not using default):**
```bash
databricks bundle run test_databricks_asset_bundles_job --target prod
```

**Run with no specific resource (shows available options):**
```bash
databricks bundle run
```

**Run with job parameters:**
```bash
databricks bundle run test_databricks_asset_bundles_job -- --param1 value1 --param2 value2
```

**Run pipeline with refresh options:**
```bash
databricks bundle run test_databricks_asset_bundles_pipeline --refresh-all
```
## Configuration Files Explained

### `databricks.yml` - Main Bundle Configuration

This is the central configuration file that defines your bundle. See the actual file: [`databricks.yml`](./databricks.yml)

**Key features:**
- **Development target**: Uses environment variables for authentication, development mode with prefixed resources
- **Production target**: Uses service principal authentication with client credentials, shared workspace with group-based permissions
- **Resource inclusion**: Automatically includes all YAML files from `resources/` directory
- **Optimized compute**: Jobs use shared autoscaling clusters for cost optimization, pipelines use serverless
- **Permission management**: Group-based permissions for simplified deployment

### `resources/test_databricks_asset_bundles.job.yml` - Job Definition

Defines a multi-task job with dependencies. See the actual file: [`resources/test_databricks_asset_bundles.job.yml`](./resources/test_databricks_asset_bundles.job.yml)

**Key features:**
- **Multi-task workflow**: Notebook → Pipeline → Python wheel execution
- **Task dependencies**: Sequential execution with proper dependency management
- **Scheduled execution**: Daily trigger configuration
- **Shared cluster**: Autoscaling cluster definition used across tasks to avoid configuration drift
- **Production deployment**: Deployed using service principal authentication

### `resources/test_databricks_asset_bundles.pipeline.yml` - Pipeline Definition

Defines a Delta Live Tables (DLT) pipeline. See the actual file: [`resources/test_databricks_asset_bundles.pipeline.yml`](./resources/test_databricks_asset_bundles.pipeline.yml)

**Key features:**
- **DLT pipeline**: Delta Live Tables for data transformation
- **Dynamic schema**: Environment-specific schema naming
- **Notebook integration**: DLT notebook as pipeline source
- **Serverless compute**: Automatic scaling and cost optimization
- **User ownership**: Pipelines owned by authenticated user (not service principal)

## CI/CD Pipeline

This project includes a complete CI/CD pipeline using GitHub Actions that automatically tests, validates, and deploys your Databricks Asset Bundle.

### Pipeline Overview

```mermaid
graph LR
    A[Push to Feature Branch] --> B[CI: Test & Validate]
    B --> C[Create Pull Request]
    C --> D[Code Review]
    D --> E[Merge to Main]
    E --> F[CD: Deploy to Production]
    F --> G[Production Environment]
```

### Continuous Integration (CI)

**Triggers:** Pull requests and pushes to feature branches

**What it does:**
- ✅ Sets up Python 3.11 environment
- ✅ Installs Python build dependencies (wheel, setuptools)
- ✅ Installs the new Databricks CLI (not pip package)
- ✅ Installs dependencies from requirements-dev.txt
- ✅ Runs unit tests with pytest (Databricks Connect tests skipped in CI)
- ✅ Performs code linting (flake8, black) using configuration files
- ✅ Validates bundle configuration with development secrets

### Continuous Deployment (CD)

**Triggers:** Pushes to main branch (after PR merge)

**What it does:**
- 🚀 Installs Python build dependencies (wheel, setuptools)
- 🚀 Installs the new Databricks CLI with bundle support
- 🚀 Validates production configuration with service principal authentication
- 🚀 Deploys to production environment using service principal
- 🚀 Uses optimized compute for cost efficiency
- 🚀 Requires manual environment approval (security gate)
- 🚀 Uses proper service principal credentials for secure deployment

### Key Implementation Details

**Authentication Strategy:**
- **Development**: Environment variables `DATABRICKS_HOST` and `DATABRICKS_TOKEN` (user token)
- **Production**: Service principal authentication using `DATABRICKS_CLIENT_ID` and `DATABRICKS_CLIENT_SECRET`
- **No profile configuration in bundle** - CLI reads environment variables automatically

**Code Quality:**
- **Configuration files**: `.flake8` and `pyproject.toml` for consistent linting
- **Test strategy**: Skip Databricks Connect tests in CI (local development only)
- **Security**: All secrets properly configured in GitHub Environments

**CLI Requirements:**
- **New Databricks CLI** (v0.240.0+) with bundle support
- **Not the old** `databricks-cli` pip package
- **Installation via official installer** in CI/CD workflows

### GitHub Environment Setup

The pipeline uses GitHub Environments for secure secret management:

**Environment Authentication Mapping:**
```
Development Environment:
DATABRICKS_DEV_HOST → DATABRICKS_HOST → Auto-detected
DATABRICKS_DEV_TOKEN → DATABRICKS_TOKEN → Auto-detected

Production Environment:
DATABRICKS_PROD_HOST → DATABRICKS_HOST → Auto-detected  
DATABRICKS_CLIENT_ID → Service Principal App ID → Auto-detected
DATABRICKS_CLIENT_SECRET → Service Principal Secret → Auto-detected
```

#### Development Environment Secrets
```
DATABRICKS_DEV_HOST = https://your-workspace.azuredatabricks.net
DATABRICKS_DEV_TOKEN = <your-development-token>
```

#### Production Environment Secrets
```
DATABRICKS_PROD_HOST = https://your-workspace.azuredatabricks.net
DATABRICKS_CLIENT_ID = <your-service-principal-application-id>
DATABRICKS_CLIENT_SECRET = <your-service-principal-client-secret>
```

**⚠️ Important:** All these should be configured as **Secrets**, not Variables, for security.

### Service Principal Configuration

For production deployments, this project uses service principal authentication with **group-based permission management**:

**Why Group-Based Permissions?**
- **Avoids hardcoding service principal names**: No need to specify exact service principal names in configuration
- **Flexibility**: Works with any service principal that's a member of the specified group
- **Simplicity**: Reduces configuration complexity and potential naming conflicts
- **Best Practice**: Follows Databricks recommendations for scalable permission management

**Key Configuration:**
- **Service Principal Authentication**: CLIENT_ID/CLIENT_SECRET environment variables
- **Shared workspace**: Uses `/Workspace/Shared/.bundle/` path with group-based permissions
- **Permission Strategy**: Uses `users` group for CAN_MANAGE permissions
- **No explicit service principal references**: Avoids dependency on specific service principal names

**Setting up Service Principal:**
1. **Create Service Principal** in Databricks workspace admin console
2. **Get Application ID** - this becomes your `DATABRICKS_CLIENT_ID`
3. **Generate Client Secret** - this becomes your `DATABRICKS_CLIENT_SECRET`
4. **Add to Users Group** - ensure the service principal is a member of the `users` group (or whatever group you specify in permissions)
5. **Grant Workspace Access** - ensure the service principal has access to create resources in your workspace
6. **Update GitHub Secrets** - add the three secrets to your production environment

**Why This Approach Works Better:**
- ✅ **No service principal name dependencies**: Bundle doesn't need to know the exact service principal name
- ✅ **Works with any service principal**: As long as it's in the specified group
- ✅ **Deployment recommendation ignored safely**: The CLI warning about explicit service principal permissions is not relevant for group-based permissions
- ✅ **Easier to maintain**: No hardcoded names in configuration files
- ✅ **Environment agnostic**: Same configuration works across different workspaces

### Workflow Commands

```bash
# Create feature branch
git checkout -b feature/new-pipeline

# Make changes and commit
git add .
git commit -m "feat: add new data pipeline"

# Push and create PR
git push -u origin feature/new-pipeline

# After PR approval and merge to main
# → Automatic production deployment
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

### Local Development
1. **Make changes** to your code, notebooks, or configurations
2. **Validate** the bundle: `databricks bundle validate`
3. **Deploy** to dev: `databricks bundle deploy --target dev`
4. **Test** your resources: `databricks bundle run <resource>`

### CI/CD Workflow
1. **Create feature branch**: `git checkout -b feature/my-feature`
2. **Make changes** and commit: `git commit -m "feat: description"`
3. **Push branch**: `git push -u origin feature/my-feature`
4. **Create Pull Request** → Triggers CI pipeline
5. **Code review and approval**
6. **Merge to main** → Triggers CD pipeline → Production deployment

### Testing Strategy
- **Unit tests**: Python code testing with pytest
- **Bundle validation**: Configuration syntax and logic checks
- **Integration tests**: End-to-end pipeline validation (optional)
- **Production verification**: Post-deployment health checks

## Key Benefits Demonstrated

- **Serverless Computing**: Automatic scaling, cost optimization, no cluster management overhead
- **Environment Isolation**: Separate dev/prod configurations with different authentication methods
- **Dependency Management**: Jobs can depend on pipeline completion
- **Infrastructure as Code**: All resources defined in version-controlled YAML
- **Automated Building**: Python packages built and deployed automatically
- **Resource References**: Pipeline IDs dynamically referenced in jobs
- **CI/CD Integration**: Automated testing, validation, and deployment
- **Security**: Service principal authentication with group-based permission management for production
- **Code Quality**: Automated linting and testing
- **Approval Gates**: Production deployments require manual approval
- **Simplified Permissions**: Group-based permissions that avoid service principal name resolution issues

## Troubleshooting

**Validation Errors:**
```bash
databricks bundle validate
```

**Check CLI Version:**
```bash
databricks --version
# Should show v0.240.0 or later for bundle support
```

**CLI Installation Issues:**
- ❌ `Error: No such command 'bundle'` → You have the old CLI installed
- ✅ **Solution:** Install the new CLI using the official installer (not pip)
- ✅ **Remove old CLI:** `pip uninstall databricks-cli`

**Authentication Issues:**
- ❌ `cannot parse config file: open ~/.databrickscfg: no such file or directory`
- ✅ **Solution:** Use environment variables instead of profile in CI/CD
- ✅ **For local development:** Run `databricks configure` or set environment variables

**Check Deployed Resources:**
```bash
databricks bundle summary --target dev
```

**View Logs:**
Check the Databricks workspace under **Workflows** for job execution details.

**CI/CD Pipeline Issues:**
- Check GitHub Actions logs in the repository's Actions tab
- Verify environment secrets are correctly configured as **Secrets** (not Variables)
- Ensure service principal has proper permissions for production
- Verify you're using the new Databricks CLI in workflows

**Common Issues:**
- **Build errors**: Missing wheel package → Fixed automatically by installing build dependencies
- **Catalog not found**: Create the required catalog in your workspace
- **Permission denied**: Verify token/service principal permissions and group membership
- **Bundle validation fails**: Check YAML syntax and resource references
- **Variable interpolation warnings**: Don't use `${VAR}` syntax for authentication fields (`host`)
- **Workspace path access**: Using secure service principal paths with group-based permissions
- **CLI permission recommendations**: The CLI may recommend adding explicit service principal permissions, but this can be safely ignored when using group-based permissions like we do with the `users` group

**About the CLI Permission Recommendation:**
When deploying, the Databricks CLI may show a recommendation like:
```
Recommendation: permissions section should explicitly include the current deployment identity 'service-principal-name' or one of its groups
```

**This recommendation can be safely ignored** when using group-based permissions because:
- The service principal gets permissions through group membership (`users` group in our case)
- Group-based permissions are more flexible and maintainable than explicit service principal permissions
- The deployment will work correctly despite the recommendation
- This approach avoids hardcoding service principal names in configuration files

## Next Steps

- **✅ CI/CD Pipeline**: Already implemented with GitHub Actions
- **✅ Optimized Compute**: Jobs configured with single-node clusters for cost optimization, pipelines use serverless
- **Add more complex workflows** with multiple dependencies
- **Integrate with ML workflows** using MLflow
- **Explore advanced bundle features** like shared clusters and permissions
- **Add integration tests** for end-to-end validation
- **Implement blue-green deployments** for zero-downtime releases
- **Add monitoring and alerting** for production pipelines

### Current Compute Configuration

The project is configured for optimal performance and cost:

**Jobs**: Use shared autoscaling cluster (1-2 workers) to avoid configuration drift and optimize costs
**Pipelines**: Configured with `serverless: true` for Delta Live Tables

**Benefits Realized**:
- ⚡ **Quick startup**: Small autoscaling clusters start faster than large clusters
- 💰 **Cost optimization**: Minimal compute resources, shared across tasks, autoscales based on workload
- 🔄 **DLT Serverless**: Pipelines use true serverless compute with auto-scaling
- 🛠️ **Configuration consistency**: Single cluster definition prevents drift between tasks
- 🔒 **Secure deployment**: Service principal authentication for production deployments

## Additional Resources

- **Official Documentation**: [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- **VS Code Extension**: [Databricks Extension](https://docs.databricks.com/dev-tools/vscode-ext.html) for local development
- **Databricks Connect**: [Setup Guide](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) for local testing
- **Deployment Modes**: [Understanding Dev vs Prod](https://docs.databricks.com/dev-tools/bundles/deployment-modes.html)
- **GitHub Actions**: [Databricks CI/CD](https://docs.databricks.com/dev-tools/ci-cd/ci-cd-github.html) integration guide
- **Service Principals**: [Authentication Setup](https://docs.databricks.com/dev-tools/service-principals.html) for production

---

*This project demonstrates enterprise-grade Infrastructure as Code with Databricks, featuring automated CI/CD pipelines, serverless compute for optimal cost and performance, multi-environment deployments, and security best practices for production data and ML workloads.*
