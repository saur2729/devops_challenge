# DevOps Challenge - Validator Node

Node.js validator service designed to run in a detached process or natively inside Docker.

---

## 🚀 Setup and Launch (New Python Automation)

The easiest and most robust way to configure this node is using the new Python automation scripts. They automatically handle system dependencies (like Git and Node.js v22+), environment variables, logs, and process locks on both Linux and macOS.

### 1. Fully Automated Install
Use the bootstrap script on a fresh machine to install Git, clone this repository, and immediately launch the background application:

```bash
python3 install.py
```
*Optional:* You can specify a custom installation directory using the `-w` flag:
```bash
python3 install.py -w /opt/validator
```

### 2. Local Setup Only
If you have already cloned the repository and skipped the bootstrap script, you can run the localized setup script directly from the root of the project to check Node.js versions, install dependencies, and run the background app:

```bash
python3 setup.py
```

---

## 🐢 Setup and Launch (Legacy Bash Scripts)

If you prefer using the legacy bash scripts, they are still available:

1. **Full Bootstrap** (Requires manual Git installation):
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
2. **Local Setup Only**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

Ensure you configure `.env` from `.env_example` manually if handling deployments without the scripts.

---

## 🐳 Docker Deployment

This project includes a production-ready `Dockerfile` running on a minimal `node:22-alpine` image. 

It is fully integrated with a GitHub Actions workflow located at `.github/workflows/docker-publish.yml` that automatically builds, tags, and pushes the image to the GitHub Container Registry (GHCR) upon every push to the `main` branch.

---

## 💻 Development

- **Run in Dev Mode**
  ```bash
  npm install
  npm run dev
  ```
- **Build and Run**
  ```bash
  npm start
  ```

---

## 📂 Project Structure

```
devops-challenge-sh/
├── install.py         # Advanced Python bootstrap installer
├── setup.py           # Advanced Python local environment setup
├── common/
│   └── utils.py       # Shared Python utilities for logging and commands
├── install.sh         # Legacy bootstrap script
├── setup.sh           # Legacy setup script
├── Dockerfile         # Alpine-based Node 22 containerization
├── .github/
│   └── workflows/
│       └── docker-publish.yml # CI/CD automated build and push to GHCR
├── .env_example       # Environment variables template
├── package.json        
├── package-lock.json
├── .gitignore
└── src/
    └── app.js         # Express server on port 3000
```

---

## 🛠️ Requirements

- **Node.js 22+** (Auto-installed by scripts)
- **Python 3+** (For automated installation)
- **Bash** (For legacy script execution)
