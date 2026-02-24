### Setup and Launch

Run the app using the provided scripts:

```bash
chmod +x setup.sh
./setup.sh
```

Ensure you configure `.env` from `.env_example`.

#### Development

- Run in Dev Mode

```bash
npm install
npm run dev
```

- Build and Run

```bash
npm start
```

## Project Structure

```
devops-challenge-sh/
├── setup.sh           # Setup script
├── install.sh         # Installation script to set up and run on the client node
├── .env_example       # environment variables here
├── package.json        
├── package.lock.json
├── .gitignore
└── src/
    └── app.js          # Express server on port 3000

```

---

## Requirements

- Node.js 22+
- Bash (for script execution)

---
