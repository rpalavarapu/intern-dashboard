# gitlab-wrapper

A Python-based toolkit to interact with GitLab APIs on Swecha's self-hosted GitLab instance ([code.swecha.org](https://code.swecha.org)).  
It includes utilities to authenticate with GitLab, fetch and validate `.vscode/settings.json` files from repositories, and ensure contributors follow standard development practices.



## 📁 Project Structure

```
gitlab-wrapper/
├── main.py                 # Entry point (stub for future logic)
├── vscode_validation.py   # Validates developer environment settings
├── requirements.txt       # Python dependencies (to be added)
└── .env                   # Stores your GitLab ACCESS_TOKEN (not committed)
```


## 🚀 Features

- 🔐 Authenticates via GitLab personal access token  
- 🌐 Fetches `.vscode/settings.json` from GitLab raw URLs  
- ✅ Validates:
  - Git, Python, and uv version requirements
  - Required Python packages (`numpy`, `pandas`, `streamlit`)
  - Required VS Code extensions
- 🧪 Prints detailed pass/fail feedback for each item



## 📦 Installation

```bash
git clone https://code.swecha.org/ranjithraj/gitlab-wrapper.git
cd gitlab-wrapper
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add your GitLab access token:

```env
ACCESS_TOKEN=your_gitlab_private_token_here
```



## 🧪 Test and Deploy

### ✅ Testing

For now, the project includes scripts that are designed to be run manually and tested with different GitLab `.vscode/settings.json` inputs.

#### Manual Test Example:

```bash
python vscode_validation.py
```

Provide a valid GitLab raw URL when prompted. Verify output like:

```
✅ tool: version satisfied
❌ missing package or extension
```



### 🧠 Deployment

This tool is primarily CLI-based, but we plan to:

- Package it as a Python module (`pip install gitlab-wrapper`)
- Deploy a companion Streamlit UI for non-technical users
- Optionally containerize the tool with Docker for scalable deployment



## 💬 Support

Need help or have a question about `gitlab-wrapper`?

- 🐛 **Found a bug?**  
  [Open an issue](https://code.swecha.org/ranjithraj/gitlab-wrapper/-/issues) with steps to reproduce it.

- 💡 **Have a feature request or idea?**  
  Feel free to [create a new issue](https://code.swecha.org/ranjithraj/gitlab-wrapper/-/issues) labeled `feature`.

- 📧 **Need help with setup or usage?**  
  Reach out via email: **contact@swecha.org**

- 👥 **Collaborating as part of a Swecha initiative?**  
  Join the internal coordination channel or get in touch with your mentor for technical guidance.



# Contributing to gitlab-wrapper

🎉 Thank you for considering contributing to `gitlab-wrapper` — a tool built to streamline GitLab automation and developer environment validation on [code.swecha.org](https://code.swecha.org)!

We welcome all kinds of contributions: code, documentation, bug reports, feature requests, ideas, and feedback.


## 🧰 Prerequisites

- Python 3.8+
- A GitLab account on [code.swecha.org](https://code.swecha.org)
- Git installed
- A GitLab **Access Token** with `api` scope (store it in a `.env` file as `ACCESS_TOKEN=your_token`)



## 🛠 Setting Up the Project

1. **Fork** the repository on [code.swecha.org](https://code.swecha.org).
2. Clone your forked repo:

```bash
git clone https://code.swecha.org/your-username/gitlab-wrapper.git
cd gitlab-wrapper
```
<br>



## 📝 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software for any purpose, as long as the original license and copyright notice are included.

See the [LICENSE](LICENSE) file for the full text.