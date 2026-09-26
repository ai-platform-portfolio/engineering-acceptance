export function credentialLabel(host: string, username: string): string {
  const cleanHost = host.trim().toLowerCase();
  const cleanUser = username.trim();
  if (!cleanHost) {
    throw new Error("Host is required");
  }
  if (!cleanUser) {
    throw new Error("Username is required");
  }
  if (cleanHost.includes("/") || cleanUser.includes("@")) {
    throw new Error("Invalid connection identity");
  }
  return `${cleanUser}@${cleanHost}`;
}
