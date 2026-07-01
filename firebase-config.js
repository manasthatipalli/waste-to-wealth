import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { getStorage } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-storage.js";

const firebaseConfig = {
  apiKey: "AIzaSyDxB0CLTALlerx0nRkmUzKpzcgqS8rjIHw",
  authDomain: "wtow-new-2026.firebaseapp.com",
  projectId: "wtow-new-2026",
  storageBucket: "wtow-new-2026.firebasestorage.app",
  messagingSenderId: "902721287811",
  appId: "1:902721287811:web:9134d99dcecee60e150db6"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

export { app, auth, db, storage };
