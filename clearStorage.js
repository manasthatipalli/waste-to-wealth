const admin = require("firebase-admin");

let serviceAccount;
try {
  serviceAccount = require("./serviceAccountKey.json");
} catch (e) {
  console.warn("WARNING: 'serviceAccountKey.json' not found. Please place it in this directory to authenticate Firebase Admin.");
}

if (serviceAccount) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    storageBucket: "YOUR_STORAGE_BUCKET_NAME.appspot.com"
  });

  const bucket = admin.storage().bucket();

  async function deleteAllFiles() {
    try {
      console.log("Starting deletion of all physical images in Firebase storage (prefix: submissions/)...");
      await bucket.deleteFiles({ prefix: "submissions/" });
      console.log("SUCCESS: All physical images have been deleted. Your storage quota will clear shortly!");
    } catch (error) {
      console.error("Error deleting files:", error);
    }
  }

  deleteAllFiles();
} else {
  console.log("Firebase Admin could not be initialized because serviceAccountKey.json is missing.");
}