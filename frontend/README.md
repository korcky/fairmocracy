# Web app info

**What is this:**  
This is a Svelte/SvelteKit web application for our project's frontend. This README provides detailed instructions to help you set up your environment, install dependencies, and get started with development.

---

## Prerequisites

Ensure you have the following installed before contributing:

- **npm, Node.js:**
  - The recommended approach for installing npm (and Node.js) is installing a Node Version Manager (nvm), which allows you to install multiple versions of Node.js and npm. You can install nvm on Windows, macOS, and Linux -- the installation instructions are available at https://github.com/nvm-sh/nvm.

    Node version used is the latest LTS version which you can get after installing **nvm** by running:
    ```bash
    nvm install --lts
    ```

---

## Getting Started

1. **Install Dependencies**

   In the `frontend` folder, install all required packages:

   ```bash
   npm install
   ```

2. **Environment Configuration**

   - [Not needed at the moment] Create a `.env` file in the `/frontend` directory (if needed) based on the provided `.env.example` template.
   - This file is used to store environment-specific variables and should not contain sensitive production data.

---

## Development Workflow

- **Start the Development Server:**

  ```bash
  npm run dev
  ```

  To automatically open the app in your browser:

  ```bash
  npm run dev -- --open
  ```

- **Linting & Formatting:**

  - Check code formatting with Prettier:

    ```bash
    npm run format
    ```

  - Run ESLint to check for code issues:

    ```bash
    npm run lint
    ```

- **Testing:**

  Run unit tests using Vitest:

  ```bash
  npm run test
  ```

---

## Building for Production

To create a production build of your application:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

