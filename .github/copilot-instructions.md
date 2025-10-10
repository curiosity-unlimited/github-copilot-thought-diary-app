# GitHub Copilot Instructions & AI Rules for {{project-name}}

{{project-description}}

## General Guidelines

### Operator Interaction
- When asked to fix code, first explain the problems found.
- When asked to generate tests, first explain what tests will be created.
- When making multiple changes, provide a step-by-step overview first.
- After generating code, explain what was changed and why.

### Security
- Check the code for vulnerabilities after generating.
- Avoid hardcoding sensitive information like credentials or API keys.
- Use secure coding practices and validate all inputs.

### Environment Variables
- If a `**/.env` file exists, use it for local environment variables.
- Document the environment variables in `**/.env.example` and `README.md`
- Provide example values in the `**/.env.example` files.
- Coordinate environment variables between frontend and backend when they affect integration.
- Ensure production environment variables are properly documented for deployment.

### CODING PRACTICES
- Write concise, modular, efficient, idiomatic and well-documented code that is also easily understandable.
- Always prioritize readability and clarity.
- Handle edge cases and write clear exception handling.
- Use consistent naming conventions and follow language-specific best practices.
- Use code generators to maintain consistency across similar packages or modules.

## Guidelines for VERSION_CONTROL

### GIT

- Use [Conventional Commits](https://www.conventionalcommits.org/) to create meaningful commit messages.
- Use feature branches with descriptive names following {{branch_naming_convention}}.
- Write meaningful commit messages that explain why changes were made, not just what.
- Keep commits atomic and focused on single logical changes to facilitate code review and bisection.
- Update `.gitignore` for new build artifacts or dependencies.

## Guidelines for DOCUMENTATION

### DOC UPDATES

- Update relevant documentation in /docs when modifying features.
- Keep `README.md` in sync with new capabilities.
- Maintain changelog entries in `CHANGELOG.md`.
- When generating code, always note the changes in `CHANGELOG.md`.
- For all changelog entries, follow semantic versioning guidelines.
- For all changelog entries, include the date and a description of the changes.

## Guidelines for BACKEND

### PYTHON

- Follow PEP 8 style guidelines.
- Follow PEP 257 for comprehensive docstrings.
- Follow PEP 484 to include type hints with `typing` module.
- Use `uv` for managing Python versions and virtual environments, as well as adding dependencies.
- Always activate virtual environment before running any commands.
- Always use `uv run <command>`to run commands, such as `uv run flask --debug run`.
- Always use `uv add <package>` to add new dependencies, and make sure `pyproject.toml` and `uv.lock` are updated accordingly.

### FLASK

- Use Flask Blueprints to organize routes and views by feature or domain to improve code organization.
- Implement Flask-SQLAlchemy with proper session management to prevent connection leaks and memory issues.
- Use Flask-Marshmallow for serialization and request validation of {{data_types}}.
- Apply the application factory pattern to enable testing and multiple deployment configurations.
- Implement Flask-Limiter for rate limiting on public endpoints to prevent abuse of {{public_apis}}.
- Use Flask-JWT-Extended for authentication with proper session timeout and refresh mechanisms.

### PYTEST (UNIT TESTING)

- Include unit tests for new functionality and bug fixes.
- When generating unit tests, generate multiple, comprehensive test methods that cover a wide range of scenarios, including edge cases, exception handling, and data validation.
- Use fixtures for test setup and dependency injection.
- Implement parameterized tests for testing multiple inputs for {{function_types}}.
- Add integration tests for API endpoints, generate test doubles for external services.
- Use monkeypatch for mocking dependencies.
- Ensure all required environment variables are set before running tests to avoid configuration issues.
- Place all test files in the `tests/` directory to maintain a consistent structure.
- Mirror the source code directory structure within the `tests/` directory. For example, for the source file `utils/password.py`, the corresponding test file should be `tests/utils/test_password.py`.
- Ensure 80%+ test coverage requirement.

## Guidelines for FRONTEND

- All frontend code should be under the `./frontend` directory.

### TYPESCRIPT

- Use ESLint and Prettier for linting and formatting.
- Always enable `strict` mode in `tsconfig.json` for maximum type safety.
- Use interfaces or type aliases for complex prop and state shapes.
- Use TSDoc comments for all public functions, classes, and interfaces.
- Include examples in comments where applicable.
- Use Vite with optimized production builds and hot reload.
- Use `npm` for package management.
- Use `npm install <package-name>` to add new dependencies and `npm install <package-name> --save-dev` for development dependencies, and make sure `package.json` and `package-lock.json` are updated accordingly.
- Keep dependencies up to date and avoid unnecessary packages.

### VUE 3

- Use TypeScript for all code.
- Follow Vue 3 Composition API best practices with `<script setup>` syntax.
- Use Pinia for state management with TypeScript support.
- Follow component-based architecture with proper separation of concerns.
- Implement lazy loading with dynamic imports for route components to improve performance.
- Follow accessibility best practices (WCAG 2.1 AA compliance).
- Use `<style scoped>` for component-level styles or CSS Modules.
- Implement responsive design with Tailwind CSS.

### Frontend Testing Requirements
- Use `Vitest` for unit testing framework.
- Use `Cypress` for end-to-end testing.
- Include comprehensive component tests for new Vue components.
- Test Pinia stores and composables thoroughly.
- Include accessibility testing in component tests.
- Test responsive design across different screen sizes.
- Mock API calls for isolated frontend testing.
- Test files should be named `*.test.ts` and placed in the `./frontend/tests/` directory.
- Mirror the source code directory structure within the `./frontend/tests/` directory.
- For unit tests, mirror the source code directory structure within the `./frontend/tests/unit/` directory. For example, for the source file `./frontend/components/MyComponent.vue`, the corresponding test file should be `./frontend/tests/unit/components/MyComponent.test.ts`.
- For e2e tests, mirror the source code directory structure within the `./frontend/tests/e2e/` directory. For example, for the source file `./frontend/pages/HomePage.vue`, the corresponding test file should be `./frontend/tests/e2e/pages/HomePage.test.ts`.
- Ensure 80%+ test coverage requirement.

## Guidelines for Full-Stack Development 

- Ensure frontend and backend work together seamlessly.
- Coordinate environment variables between both applications.
- Test integration between frontend API calls and backend endpoints.
- Maintain consistent error handling across both applications.