# Repository Overview

## Structure

This repository is organized into two main sections:

1. **APIs**: 
   - Contains the code for all APIs. This is where API development and maintenance take place.
  
2. **Research**: 
   - Contains all Proofs of Concept (POCs). These may include Jupyter notebooks or Python scripts that are used for exploratory research and development.

## Branching Strategy

Our repository follows a strict branching hierarchy:

- **Task Branch**: 
  - Each task or feature should have its own dedicated branch.
  
- **Development Branch**: 
  - All task branches are merged into this branch once they meet the acceptance criteria for the task.
  
- **Master Branch**: 
  - The final branch that holds the stable and production-ready code. 

### Merging Rules

- **Merging into the Development Branch**: 
  - PRs must meet the task acceptance criteria before being merged into the development branch.
  
- **Merging into the Master Branch**: 
  - A merge into the master branch must be approved by either **Giuliano** or **Morgana**.

Please follow this workflow to ensure a smooth development process.
