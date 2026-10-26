# SecureDoc frontend design brief

## Objective
Create the frontend for SecureDoc, a local SHA-256 document integrity verification dashboard for a beginner-friendly academic demonstration. The app must feel like a real security operations workspace, not a tutorial.

## Audience and aesthetic
The audience is a college panel and local users who need clear evidence of document integrity. Use a precise, editorial security-dashboard aesthetic: deep ink/navy sidebar, warm off-white canvas, royal blue actions, thin blue-gray borders, and restrained green/amber/red semantic states. Favor strong typography, compact information density, and a distinctive blue verification accent rather than generic gradients.

## Structure
Implement a responsive app shell with:
- persistent desktop sidebar and compact mobile navigation
- header with page context, global document search, and system status
- routes for Dashboard, Register, Verify, Document Records, Verification History, Settings, and About
- reusable cards, buttons, tables, status badges, dialogs, empty states, loading states, and toast feedback
- real API integration through a central service; no fake statistics or sample data

Dashboard should prioritize four statistics, quick actions, recent activity, and a verification chart. Registration should guide users through select → hash → confirm reference. Verification should make the reference/current hash comparison visually unmistakable. Records and history should be practical tables with search/filter/pagination. Settings/About should explain behavior and limitations clearly.

## Typography and visual language
Use a local/system font stack with a technical monospace treatment for hashes. Use uppercase micro-labels sparingly, rounded 10–14px cards, subtle shadows, and generous but efficient spacing. Icons must come from lucide-react. Use CSS variables/design tokens, accessible focus rings, reduced-motion support, and responsive layouts at 1440, 1024, 768, and 390px.

## Image needs
No photos or external images are needed. Use lucide icons and CSS geometry only; avoid remote font/image dependencies.

## Output
Implement directly in the project’s `frontend/` directory and integrate with the Flask API at `http://127.0.0.1:5000/api` via Vite proxy. Keep the frontend understandable and maintainable for a beginner.
