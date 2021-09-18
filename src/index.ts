// Use the Client that are provided by @typeit/discord NOT discord.js
import {
  Discord,
  On,
  Client,
  Command,
  CommandMessage,
  CommandNotFound
} from "@typeit/discord";

const start = async () => {
  const client = new Client({
    classes: [
      `${__dirname}/*Discord.ts`, // glob string to load the classes
      `${__dirname}/*Discord.js` // If you compile using "tsc" the file extension change to .js
    ],
    silent: false,
    variablesChar: ":"
  });

  await client.login("YOUR_TOKEN");
}

start();

// Specify your prefix
@Discord("!") 
abstract class AppDiscord {
  // Reachable with the command: !hello
  @Command("hello")
  private hello(message: CommandMessage) {
  }

  // !bye
  // !yo
  @CommandNotFound()
  private notFound(message: CommandMessage) {
  }
}
