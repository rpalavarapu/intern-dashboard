
# Contributing to gitlab-wrapper

🙏 Thank you for your interest in contributing to `gitlab-API-wrapper`!  
This project is built to simplify GitLab automation and developer environment validation for [code.swecha.org](https://code.swecha.org), and we welcome your ideas, feedback, and code.



## 📋 Table of Contents

- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Code of Conduct](#code-of-conduct)

---

## 💡 How to Contribute

You can contribute in several ways:

- 💻 Add new features (e.g., visualizations, filters)
- 🐛 Fix bugs or optimize performance
- 🧪 Write or improve tests
- 📖 Enhance documentation

---

## ⚙️ Development Setup

1. **Fork and Clone the Repository**
    ```bash
    git clone https://code.swecha.org/Soham/internship-dashboard.git
    cd internship-dashboard
    ```

2. **Set Up a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the App**
    ```bash
    streamlit run Intern_Dashboard.py
    ```

---

## 🧑‍💻 Coding Guidelines

- Follow Python PEP8 standards.
- Use `ruff` for linting and formatting:
    ```bash
    ruff check .
    ```
- Keep functions modular and readable.
- Reuse components where possible.
- Avoid hardcoding GitLab tokens or sensitive data.

---

## 🚀 Pull Request Process

1. Create a feature or fix branch:
    ```bash
    git checkout -b feature/add-xyz
    ```

2. Make your changes and test thoroughly.

3. Commit with a clear message:
    ```bash
    git commit -m "✨ Added commit size graph by user"
    ```

4. Push your branch:
    ```bash
    git push origin feature/add-xyz
    ```

5. Open a **Merge Request** at:
   [https://code.swecha.org/Soham/internship-dashboard/-/merge_requests](https://code.swecha.org/Soham/internship-dashboard/-/merge_requests)

---

## 🐞 Reporting Issues

Please use the [Issues tab](https://code.swecha.org/Soham/internship-dashboard/-/issues) to report:

- Bugs 🐛
- Feature Requests 🌟
- Documentation Gaps 📄

Include:
- What happened?
- What did you expect?
- Steps to reproduce
- Screenshots or logs (if available)

---

## 🤝 Code of Conduct

We expect all contributors to follow our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful and inclusive.

---

Thanks for helping improve the GitLab API wrapper! 💙  
Let’s build something amazing together.


