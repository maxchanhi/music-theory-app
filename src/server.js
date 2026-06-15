const mongoose = require("mongoose");
const { createApp } = require("./app");
const { User } = require("./logic/auth");

const port = process.env.PORT || 8080;

async function ensureDatabase() {
  if (process.env.MONGO_URI) {
    // An external MongoDB is configured; use it as-is.
    return false;
  }

  // No external MongoDB configured. Spin up an in-memory MongoDB so the app
  // can run out of the box (e.g. in the Replit dev environment). For a
  // persistent/shared database, set the MONGO_URI environment variable.
  const { MongoMemoryServer } = require("mongodb-memory-server");
  const mongod = await MongoMemoryServer.create();
  process.env.MONGO_URI = mongod.getUri("music_theory");
  console.log("Started in-memory MongoDB (set MONGO_URI to use a persistent database)");
  return true;
}

async function seedDemoUser() {
  try {
    const existing = await User.findOne({ user_name: "demo" });
    if (!existing) {
      await User.create({
        user_name: "demo",
        user_password: "demo",
        user_id: "demo",
      });
      console.log("Seeded demo user (username: demo / password: demo)");
    }
  } catch (error) {
    console.error(`Failed to seed demo user: ${error.message}`);
  }
}

async function bootstrap() {
  const usingInMemoryDb = await ensureDatabase();

  const app = createApp();

  // Only seed the demo user for the ephemeral in-memory database, never against
  // an externally configured (e.g. production) MongoDB.
  if (usingInMemoryDb) {
    mongoose.connection.once("connected", () => {
      seedDemoUser();
    });
  }

  app.listen(port, "0.0.0.0", () => {
    console.log(`Server listening on ${port}`);
  });
}

bootstrap();
