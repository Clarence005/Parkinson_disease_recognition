// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDO-tZu_c04Kh-YfxEXueZ5gxVtNtJQHWE",
  authDomain: "parkinsons-3c196.firebaseapp.com",
  projectId: "parkinsons-3c196",
  messagingSenderId: "593141079202",
  appId: "1:593141079202:web:49f0449f370c961f8b8bfb"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
