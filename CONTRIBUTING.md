# Contributing to Sentinel Core

First off, thank you for considering contributing to AB Labs. It's people like you that make Sentinel Core a premier choice for mission-critical surveillance.

## Institutional Standards

As a project engineered for strategic environments, we maintain high standards for code quality and architectural integrity:

1.  **Strict Typing**: All new modules must use Python type hints.
2.  **Modular Design**: Avoid monolithic classes. Favor the "Processor/Detector/Manager" pattern.
3.  **Performance Focus**: Avoid heavy dependencies. If a feature can be implemented using NumPy or pure Python, prioritize that over bulky libraries.

## Development Workflow

1.  **Fork the Repo**: Create your own tactical workspace.
2.  **Create a Branch**: Use a prefix like `feat/`, `fix/`, or `refactor/`.
3.  **Run the Demo**: Ensure your changes don't break the `demo.py` visualizer.
4.  **Submit a PR**: Provide a clear description of the technical impact of your changes.

## Code of Conduct

We are committed to a professional, institutional environment. Be respectful, be technical, and stay focused on the mission.

---

© 2026 [AB Group](https://abgroupglobal.com) • Strategic Systems Engineering.
