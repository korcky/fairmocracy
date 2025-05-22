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

---

## Current Functionality Overview

### 1. Project Structure & Routing

- **Routing** lives under `src/routes/`:
  - `/` - the main game UI (`AppCore.svelte`)
  - `/about` - static information page
  - `/admin` - admin view for uploading new game configurations, and future admin controls and statistics

### 2. State Management (Svelte Stores)

#### `gameData` store

- **Location:** `src/lib/stores/gameData.svelte.js`
- **Contents:**  
  - Game metadata (`id`, `name`, `status`)  
  - Current round/event, countdown timer  
  - List of parties and their current standings
- **Key methods:**
  - `loadParties(gameId: string)`:  
    Fetches party list from  
    ```
    GET ${PUBLIC_BACKEND_URL}/game/${gameId}/parties
    ```
  - `initGameStateSSE()`:  
    Opens a Server‐Sent Events stream:
    ```
    EventSource(${PUBLIC_BACKEND_URL}/sse/game-state)
    ```
    Listens for real‐time JSON updates to advance game state.

#### `userData` store

- **Location:** `src/lib/stores/userData.svelte.js`
- **Contents:**  
  - Current user (name, `userId`, `gameId`)  
  - Party affiliation, rewards, and other user info
- **Key methods:**
  - `setUserData(...)` : manage login and other user info 
  - `getExtraInfo()`: fetches party‐ or user‐specific details

### 3. Component Flow

- **`AppCore.svelte`** (entry point)  
  Chooses which screen/component to render based on `gameData` + `userData` (this logic is done in `src/lib/stores/screenStore.svelte.js`):
  1. **GameSelectionScreen**  
     - Prompt for game code  
     - `GET /join?game_hash=…`
  2. **RegisterScreen**  
     - Enter user name  
     - `POST /register`
  3. **RegisterToVoteScreen**  
     - Pick a party  
     - `POST /register_to_vote`
  4. **VoteInfoScreen**  
     - Shows proposal text from current event
  5. **VoteScreen**  
     - YES / NO / ABSTAIN buttons  
     - `POST /v1/voting/cast_vote`
  6. **VoteWaitScreen**  
     - Displays waiting state until a SSE update advances the game state
  7. **GameEndedScreen**  
     - Summary of results
  8. **AdminView** (at `/admin`)  
     - **`FileUpload.svelte`** for uploading a JSON config via `POST /upload_config`

### 4. API Integration

All backend calls use the `PUBLIC_BACKEND_URL` environment variable:

| Action                         | HTTP Request                              | Endpoint                     | 
|--------------------------------|-------------------------------------------|------------------------------|
| Join a game                    | `GET /join?game_hash=<code>`              | `get_game_by_hash`           |                |
| Register user                  | `POST /register`                          | `register_user`              |               |
| Choose party                   | `POST /register_to_vote`                  | `register_to_vote`           |
| Fetch parties                  | `GET /game/{gameId}/parties`              | `read_parties_by_game`       | 
| Cast vote                      | `POST /v1/voting/cast_vote`               | `cast_vote`                  | 
| Upload game config (admin)     | `POST /upload_config`                     | `upload_config`              | 

> **Note:** Endpoints decorated with `@broadcast_game_state` push real‐time updates via SSE.

### 5. Real-time Updates

- Server-Sent Events (SSE) stream at:
  ```
  GET ${PUBLIC_BACKEND_URL}/sse/game-state
  ```
- The frontend’s `initGameStateSSE()` subscribes, listens for state changes, and updates the `gameData` and `userData` stores automatically and manages UI transitions without manual polling.

### 6. Environment Variables

- **`PUBLIC_BACKEND_URL`** (in `.env`)  
  FastAPI backend URL for all API calls, e.g.:
  ```bash
  PUBLIC_BACKEND_URL="http://127.0.0.1:8000"
  ```