# OmniVision Frontend Application

OmniVision is an AI-Powered Accessibility Assistant. This frontend repository is built using **React**, **TypeScript**, and **Vite**. It heavily focuses on a modern, medium-scale desktop UI design that handles AI accessibility tasks dynamically utilizing responsive CSS boundaries.

## 🛠 Tech Stack
- **Framework:** React 18
- **Language:** TypeScript
- **Bundler:** Vite
- **Styling:** Vanilla CSS (`global.css`) utilizing Design Tokens (colors, semantic gradients, and layout shadows).
- **Icons:** Lucide React

---

## 📂 Folder Structure

The application follows a clean, component-driven modular architecture under the `src/` directory.

```text
src/
├── api/          # Directory intended for Backend API Integrations (Axios/Fetch services)
├── components/   # Reusable UI Blocks (Navbar, Tabs, Cards)
├── pages/        # Core Feature Views (GesturePage, AudioPage)
├── store/        # Directory intended for Global State Management (Redux/Context API)
├── styles/       # Global CSS definitions containing all typography and UI standardizations
├── App.tsx       # Root Component coordinating layouts and client routing
└── main.tsx      # React DOM Entry point
```

---

## 🧩 Core UI Design & Components

The application embraces a **Medium-Sized Dashboard UI Paradigm**, rendering massive immersive components rather than standard edge-to-edge web pages or hyper-constrained mobile rows.

### 1. Global Navigation (`src/components/`)
- **`Navbar.tsx`**: A heavy, robust top navigation header housing branding and live metric indicators (e.g., Active Users). 
- **`Tabs.tsx`**: Built as a thick, floating generic Segmented Control (Pill-shaped UI) capable of switching Active Pages instantly utilizing React State without page reloads.

### 2. Gesture Recognition (`src/pages/GesturePage.tsx`)
- **Purpose**: Real-time sign language / gesture detection utilizing user webcams.
- **Layout**: It incorporates a sophisticated **Dual-Column Flex Format**.
  - **Left Focus Column**: Houses the native `navigator.mediaDevices.getUserMedia` video stream mapped efficiently using `16:10` aspect ratios for rich desktop displays.
  - **Right Sidebar Column**: Encapsulates results ("Detected Gesture"), multi-language toggle pills, embedded Text-to-Speech triggers, and the Emoji-driven Gesture standard library grid.
- **Backend Touchpoints**: Currently simulates AI processing using a 2.5s timeout. The backend engineers should attach ML streams natively into `startCamera()` and return valid target mappings to replace the existing random generator.

### 3. Audio Voice Assistant (`src/pages/AudioPage.tsx`)
- **Purpose**: Dedicated voice interaction interface tailored for natural speech translation and inquiries.
- **Layout**: Operates as an **Immersive Center-stage Component** (`maxWidth: 1000px`). Sits centered on the screen providing clear focus.
- **Features**: Consists of a deeply shadowed pulsating prominent microphone recording module, an integrated "floating" language selection constraint (`EN | HI | MR`), and a sophisticated pill-shaped bottom query input.

---

## 🔗 Backend Developer Implementation Guide

To securely attach the backend backend logic and AI processing to this frontend layer:

1. **API Mapping**: Create your standard HTTP/WebSocket controllers inside `/src/api` and avoid placing fetches directly inside the `.tsx` components.
2. **Camera Streaming**: `GesturePage.tsx` initializes WebRTC. For intensive Computer Vision calculations, you should map that raw video `<canvas>` stream dynamically over WebSockets.
3. **Audio Translation Parsing**: Tie your natural language processing pipelines directly to the input submission event located inside the `/src/pages/AudioPage.tsx` interface. Ensure that native `speechSynthesisUtterance` browser APIs are maintained for playback when standardizing localized JSON responses (`'en-US'`, `'hi-IN'`, `'mr-IN'`).

---

## 🚀 Running the Project

```bash
# 1. Install standard dependencies
npm install

# 2. Start the blazing-fast Vite local development server
npm run dev

# 3. Build for production deployment 
npm run build
```

> **Note:** The local development server is configured to run automatically on **port 3000** (`http://localhost:3000/`).
