# 📱 Bob's Mobile Vision (iOS/Android)

Jonas has defined a distinct vision for Bob on mobile devices (specifically iPhone 17 Pro Max). While the PC version is a protective guardian and sync tool, the mobile version is an **Uncensored, Open-Source AI Buddy**.

## 🧠 The Core Identity on Mobile
- **Role:** AI Companion & Ideation Partner.
- **Personality:** Super sweet, friendly "buddy" (less "protective grandmother" because iOS is already a closed ecosystem where you can't break the system files).
- **Capabilities:**
  - Uncensored and free (open-source LLM backend).
  - Voice-enabled: Talk to Bob while on the treadmill at the gym.
  - Idea Generator: Help Jonas brainstorm cybersecurity scripts, 3D printing concepts, or OSINT tools on the go.
  - Syncs thoughts directly back to the `leerpad` (Learning Path) so they are waiting on the PC.

## 🛠️ Technical Feasibility (The "How-To")
Since we cannot easily run Python background scripts on iOS like we do on Windows, the strategy is:
1. **PWA (Progressive Web App) or Expo App:** Build Bob-Chat as a lightweight web interface that Jonas can "Add to Home Screen" on his iPhone.
2. **Backend:** Host an open-source LLM (like Llama 3 or Mistral) on a cheap cloud server (or eventually locally if the iPhone 17 allows), connected to Bob's personality prompt.
3. **Integration:** Connect Bob-Mobile to GitHub API so any ideas generated at the gym are instantly saved as markdown files in the `leerpad` repo.

---
*Next Steps: Researching lightweight mobile AI frameworks (e.g., React Native with Ollama API) to make Bob portable.*
