import { credentialLabel } from "../features/source-feeds/credentials";

export function sourceFeedLabel(host: string, username: string): string {
  return credentialLabel(host, username);
}
